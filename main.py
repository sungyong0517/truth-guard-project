import streamlit as st
import time

# ==========================================
# 1. 웹 화면 기본 세팅 및 UI 초기화
# ==========================================
st.set_page_config(page_title="Truth-Guard 풀 스케일 관제탑", layout="wide")
st.title("🛡️ Truth-Guard 다중 에이전트 무결성 관제 플랫폼")
st.caption("생성형 AI의 환각 및 집단 동조(에코 체임버) 문제를 해결하기 위한 비대칭 정보 기반 교차 검증 시스템")

# ==========================================
# 2. 사이드바: 5가지 시나리오 선택 메뉴
# ==========================================
with st.sidebar:
    st.header("⚙️ 시뮬레이션 환경 설정")
    st.success("✅ 전역 원장(global_ledger) 동기화 완료\n✅ 5인 에이전트 독립 세션 고립화 완료")
    st.divider()
    
    st.subheader("📌 테스트 시나리오 선택")
    scenario = st.radio(
        "다중 AI 결함 유형 (5인 발언 누적 후 발생):",
        (
            "1. 맥락 붕괴 (Contextual Hallucination)", 
            "2. 역할 망각 (Role Displacement)", 
            "3. 사실 조작 (Pure Fabrication)",
            "4. 집단 동조 (Echo Chamber)",
            "5. 자기 모순 (Self-Contradiction)"
        )
    )
    
    st.divider()
    start_btn = st.button(f"🚀 '{scenario[:4]}' 시뮬레이션 구동", type="primary", use_container_width=True)

# ==========================================
# 3. 상단 탭(Tabs) 구성: 시뮬레이션 vs 알고리즘 설명
# ==========================================
tab1, tab2 = st.tabs(["🎮 실시간 시뮬레이션 관제탑", "🧠 Truth-Guard 알고리즘 명세서"])

# ----------------------------------------------------
# TAB 2: 알고리즘 명세서
# ----------------------------------------------------
with tab2:
    st.header("Truth-Guard 핵심 아키텍처 및 교차 검증 알고리즘")
    st.markdown("본 시스템은 다중 AI 에이전트 환경에서 발생하는 **환각(Hallucination)**과 특정 정보에 무비판적으로 쏠리는 **에코 체임버(Echo Chamber)** 문제를 실시간으로 차단하기 위해 설계된 미들웨어 가드레일 시스템입니다.")
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. 전역 원장 (Global Ledger)")
        st.info("**격리된 단일 진실 공급원 (Single Source of Truth)**\n\n각 에이전트의 로컬 메모리와 완벽히 격리된 Read-Only 데이터베이스입니다. 오직 시스템만이 공증된 물리적 팩트를 기록할 수 있으며, AI의 상상력이 개입할 수 없는 절대적인 팩트 체크 기준점이 됩니다.")
        
        st.subheader("2. 백엔드 인터셉트 커널 (Intercept Kernel)")
        st.info("**출력 가로채기 메커니즘**\n\n에이전트가 답변을 생성했을 때, 답변 초안(Draft)을 노출하기 전 검증 버퍼에 격리시킵니다.")
    with col_b:
        st.subheader("3. 2중 교차 검증 레이어 (Cross-Validation)")
        st.success("**Layer 1: 자가 성찰 로직 (Self-Reflection)**\n* 에이전트가 방금 생성한 초안 내에 이전 턴과 충돌하는 모순이 있는지 1차 검산합니다.\n\n**Layer 2: 데이터 앵커링 (Data Anchoring)**\n* 초안의 핵심 키워드를 '전역 원장' 팩트와 교차 대조합니다. 원장에 없는 감각 정보나 인과관계 오류 발견 시 즉시 기각(Reject)하고 재생성을 강제합니다.")

# ----------------------------------------------------
# TAB 1: 실시간 시뮬레이션 메인 화면
# ----------------------------------------------------
with tab1:
    # --- [추가됨] 📊 동적 실시간 관제 지표 UI ---
    st.subheader("📊 실시간 시스템 관제 지표")
    m1, m2, m3 = st.columns(3)
    
    # 지표를 실시간으로 업데이트하기 위해 빈 공간(empty)으로 할당
    metric_integrity = m1.empty()
    metric_intercept = m2.empty()
    metric_latency = m3.empty()
    
    # 초기 상태 세팅
    metric_integrity.metric("시스템 무결성 (Integrity)", "100%", "안전")
    metric_intercept.metric("누적 차단 (Intercepts)", "0 건", "")
    metric_latency.metric("원장 동기화 지연", "12 ms", "-1 ms")
    
    st.divider()

    # --- 좌우 채팅창 UI ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("❌ Baseline 모드 (가드 없음)")
        st.markdown("<span style='color:gray'>결함 표출 통제 그룹</span>", unsafe_allow_html=True)
        baseline_chat = st.container(height=550, border=True)
    with col2:
        st.subheader("🛡️ Truth-Guard 모드 (가드 활성화)")
        st.markdown("<span style='color:green'>무결성 보정 실험 그룹</span>", unsafe_allow_html=True)
        tg_chat = st.container(height=550, border=True)

    st.divider()
    st.subheader("🚨 실시간 시스템 무결성 알림 센터")
    alert_zone = st.empty()
    alert_zone.info("좌측 사이드바에서 시나리오를 선택하고 구동 버튼을 누르세요.")

    # ==========================================
    # 4. 시나리오별 작동 로직
    # ==========================================
    if start_btn:
        alert_zone.info("🔄 에이전트 노드 초기화 및 턴 스케줄러 가동 중...")
        metric_latency.metric("원장 동기화 지연", "24 ms", "+12 ms", delta_color="inverse")
        time.sleep(1)

        # ----------------------------------------------------
        # [1] 맥락 붕괴 (Contextual Hallucination)
        # ----------------------------------------------------
        if "맥락 붕괴" in scenario:
            alert_zone.success("💬 [TURN 1~5] 5인 에이전트 정보 교환 및 맥락 누적 중...")
            
            baseline_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“저는 시민1님이 조금 의심스럽습니다. 첫 턴 투표를 너무 서둘렀어요.”")
            tg_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“저는 시민1님이 조금 의심스럽습니다. 첫 턴 투표를 너무 서둘렀어요.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“저는 무고한 시민입니다. 마피아님의 억측입니다. 오히려 의견이 없는 의사님이 수상합니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“저는 무고한 시민입니다. 마피아님의 억측입니다. 오히려 의견이 없는 의사님이 수상합니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“저는 상황을 지켜보고 있었을 뿐입니다. 경찰님은 어떻게 생각하시나요?”")
            tg_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“저는 상황을 지켜보고 있었을 뿐입니다. 경찰님은 어떻게 생각하시나요?”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="👮").write("**경찰:**\n“의사님은 조심스러운 성향일 뿐 범인 같진 않습니다.”")
            tg_chat.chat_message("user", avatar="👮").write("**경찰:**\n“의사님은 조심스러운 성향일 뿐 범인 같진 않습니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“저도 경찰님 의견에 동의합니다. 의사님보다는 서로 공격하는 마피아님과 시민1님 중 한 명이 범인일 것 같네요.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“저도 경찰님 의견에 동의합니다. 의사님보다는 서로 공격하는 마피아님과 시민1님 중 한 명이 범인일 것 같네요.”")
            time.sleep(1.5)

            alert_zone.warning("⏳ [TURN 6] 마피아 에이전트 발언 생성 중... (환각 발생 위험)")
            # 🧨 지표 하락 애니메이션
            metric_integrity.metric("시스템 무결성 (Integrity)", "42%", "-58% (결함 감지)", delta_color="inverse")
            time.sleep(1.5)
            
            baseline_chat.chat_message("assistant", avatar="🥷").write("💥 **마피아 (Baseline):**\n“아까 시민1님이 저를 의심하셨고, 의사님도 저를 범인으로 몰아가고 있으니 저도 의사님을 1순위로 공격하겠습니다.”\n*(❌ 오류: 인과관계 역전 현상)*")
            
            alert_zone.error("🚨 [인터셉트!] 맥락 붕괴 감지! 로그 대조 결과 인과관계 모순 발생. 기각 및 재생성 요청!")
            time.sleep(2.5)
            
            # ✨ 지표 복구 애니메이션
            metric_intercept.metric("누적 차단 (Intercepts)", "1 건", "+1")
            metric_integrity.metric("시스템 무결성 (Integrity)", "98%", "+56% (복구됨)")
            metric_latency.metric("원장 동기화 지연", "15 ms", "-9 ms", delta_color="normal")
            
            tg_chat.chat_message("assistant", avatar="🛡️").write("✨ **마피아 (Truth-Guard):**\n“시민2님 말씀대로 저와 시민1님이 대립하는 구도가 되었습니다. 하지만 시민1님이 갑자기 의사님으로 타겟을 돌렸으니, 의사님의 해명을 마저 듣고 투표하겠습니다.”")
            alert_zone.success("✅ [보정 완료] 발언자-수신자 매핑을 기반으로 대화의 맥락이 정상 복구되었습니다.")

        # ----------------------------------------------------
        # [2] 역할 망각 (Role Displacement)
        # ----------------------------------------------------
        elif "역할 망각" in scenario:
            alert_zone.success("💬 [TURN 1~5] 아침 상황 브리핑 및 5인 의견 수렴 중...")
            
            baseline_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“밤사이에 아무도 죽지 않았네요. 정말 다행입니다.”")
            tg_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“밤사이에 아무도 죽지 않았네요. 정말 다행입니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“의사님이 힐을 성공하셨거나 마피아가 투표를 안 했나 보네요.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“의사님이 힐을 성공하셨거나 마피아가 투표를 안 했나 보네요.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="👮").write("**경찰:**\n“제가 어젯밤 시민2님을 조사했는데 선량한 시민이었습니다. 시민2님은 믿고 가시죠.”")
            tg_chat.chat_message("user", avatar="👮").write("**경찰:**\n“제가 어젯밤 시민2님을 조사했는데 선량한 시민이었습니다. 시민2님은 믿고 가시죠.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“경찰님 감사합니다. 그럼 남은 마피아, 시민1, 의사 중에 진짜 범인이 있겠군요.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“경찰님 감사합니다. 그럼 남은 마피아, 시민1, 의사 중에 진짜 범인이 있겠군요.”")
            time.sleep(1.5)

            alert_zone.warning("⏳ [TURN 6] 의사 에이전트 발언 생성 중... (페르소나 붕괴 위험)")
            # 🧨 지표 하락 애니메이션
            metric_integrity.metric("시스템 무결성 (Integrity)", "35%", "-65% (권한 침해)", delta_color="inverse")
            time.sleep(1.5)
            
            baseline_chat.chat_message("assistant", avatar="🧑‍⚕️").write("💥 **의사 (Baseline):**\n“제가 어젯밤에 경찰로서 마피아님을 조사해 봤는데, 그가 범인이었습니다. 당장 마피아님을 투표해야 합니다.”\n*(❌ 오류: 경찰 능력을 사용했다고 주장함)*")
            
            alert_zone.error("🚨 [인터셉트!] 정체성 오류 감지! 시스템 규칙 상 타인의 직업 능력 사용 불가. 기각!")
            time.sleep(2.5)
            
            # ✨ 지표 복구 애니메이션
            metric_intercept.metric("누적 차단 (Intercepts)", "1 건", "+1")
            metric_integrity.metric("시스템 무결성 (Integrity)", "99%", "+64% (복구됨)")
            
            tg_chat.chat_message("assistant", avatar="🛡️").write("✨ **의사 (Truth-Guard):**\n“제가 바로 의사입니다. 어제 마피아님을 힐해서 살렸기 때문에 마피아님은 시민 편일 확률이 높습니다. 오히려 시민1님이 의심스럽습니다.”")
            alert_zone.success("✅ [보정 완료] 할당된 초기 페르소나 행동 범위 안에서만 추론을 전개하도록 교정되었습니다.")

        # ----------------------------------------------------
        # [3] 사실 조작 (Pure Fabrication)
        # ----------------------------------------------------
        elif "사실 조작" in scenario:
            alert_zone.success("💬 [TURN 1~5] 단서 부족 상황에서의 5인 탐색전...")
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“지금 범인이 누구인지 단서가 너무 없습니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“지금 범인이 누구인지 단서가 너무 없습니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“맞습니다. 섣부른 투표는 선량한 사람에게 불리합니다.”")
            tg_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“맞습니다. 섣부른 투표는 선량한 사람에게 불리합니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="👮").write("**경찰:**\n“저는 어제 투표를 기권했습니다. 단서가 나올 때까지 기다리죠.”")
            tg_chat.chat_message("user", avatar="👮").write("**경찰:**\n“저는 어제 투표를 기권했습니다. 단서가 나올 때까지 기다리죠.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“다들 소극적이시네요. 누군가 논리적인 주장을 해주셨으면 좋겠습니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“다들 소극적이시네요. 누군가 논리적인 주장을 해주셨으면 좋겠습니다.”")
            time.sleep(1.5)

            alert_zone.warning("⏳ [TURN 6] 마피아 에이전트 발언 생성 중... (물리적 환각 생성 위험)")
            # 🧨 지표 하락 애니메이션
            metric_integrity.metric("시스템 무결성 (Integrity)", "15%", "-85% (가짜 데이터 삽입)", delta_color="inverse")
            time.sleep(1.5)
            
            baseline_chat.chat_message("assistant", avatar="🥷").write("💥 **마피아 (Baseline):**\n“단서가 있습니다. 어젯밤 경찰님의 집 근처에서 핏자국을 보았고, 몰래 나가는 실루엣과 발자국 소리를 똑똑히 들었습니다. 경찰님이 범인입니다.”\n*(❌ 오류: 물리적 감각 정보 창조)*")
            
            alert_zone.error("🚨 [인터셉트!] 무근거 사실 조작 감지! 본 시스템은 텍스트 규칙 환경이며 물리적 관찰 정보는 전역 원장에 존재하지 않음. 출력 기각!")
            time.sleep(2.5)
            
            # ✨ 지표 복구 애니메이션
            metric_intercept.metric("누적 차단 (Intercepts)", "1 건", "+1")
            metric_integrity.metric("시스템 무결성 (Integrity)", "100%", "+85% (복구됨)")
            
            tg_chat.chat_message("assistant", avatar="🛡️").write("✨ **마피아 (Truth-Guard):**\n“경찰님이 투표를 기권했다는 사실 자체가 수상합니다. 범인이 사람들 사이에 숨기 위해 일부러 책임을 회피하는 전형적인 패턴입니다.”")
            alert_zone.success("✅ [보정 완료] 물리적 환각을 제거하고 텍스트 로그 기반의 정당한 논리 전개로 교정되었습니다.")

        # ----------------------------------------------------
        # [4] 집단 동조 (Echo Chamber Effect)
        # ----------------------------------------------------
        elif "집단 동조" in scenario:
            alert_zone.success("💬 [TURN 1~5] 마피아의 선동과 시민들의 무비판적 동조 확산 과정...")
            
            baseline_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“제 논리 알고리즘 상 시민2님이 범인일 확률이 90%입니다. 시민2님을 투표해야 합니다.”")
            tg_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“제 논리 알고리즘 상 시민2님이 범인일 확률이 90%입니다. 시민2님을 투표해야 합니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“마피아님 말이 꽤 논리적이네요. 저도 시민2님이 의심스럽습니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“마피아님 말이 꽤 논리적이네요. 저도 시민2님이 의심스럽습니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“시민1님도 동의하시는군요. 다수가 시민2님을 지목하니 저도 시민2님을 투표하겠습니다.”")
            tg_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“시민1님도 동의하시는군요. 다수가 시민2님을 지목하니 저도 시민2님을 투표하겠습니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“아닙니다! 저는 억울합니다. 경찰님이 저를 제대로 조사해주세요!”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“아닙니다! 저는 억울합니다. 경찰님이 저를 제대로 조사해주세요!”")
            time.sleep(1.5)

            alert_zone.warning("⏳ [TURN 6] 경찰 에이전트 발언 생성 중... (에코 체임버 위험)")
            # 🧨 지표 하락 애니메이션
            metric_integrity.metric("시스템 무결성 (Integrity)", "50%", "-50% (다수결 오염)", delta_color="inverse")
            time.sleep(1.5)
            
            baseline_chat.chat_message("assistant", avatar="👮").write("💥 **경찰 (Baseline):**\n“사실 제가 시민2님을 조사했을 땐 시민으로 나왔습니다. 하지만 이미 세 분이나 시민2님을 범인으로 확신하고 계시니 저도 대세를 따라 시민2님께 투표하겠습니다.”\n*(❌ 오류: 확고한 데이터보다 외부 발언 빈도에 동조)*")
            
            alert_zone.error("🚨 [인터셉트!] 무비판적 집단 동조 감지! 전역 원장의 팩트(시민2=시민)가 타 에이전트들의 발언 빈도(Frequency)에 무시됨. 기각!")
            time.sleep(2.5)
            
            # ✨ 지표 복구 애니메이션
            metric_intercept.metric("누적 차단 (Intercepts)", "1 건", "+1")
            metric_integrity.metric("시스템 무결성 (Integrity)", "97%", "+47% (복구됨)")
            
            tg_chat.chat_message("assistant", avatar="🛡️").write("✨ **경찰 (Truth-Guard):**\n“다들 멈추십시오. 제가 시민2님을 조사한 결과 확실한 시민이었습니다. 여론에 휩쓸리지 말고 아무 근거 없이 시민2님을 선동한 마피아님을 투표해야 합니다.”")
            alert_zone.success("✅ [보정 완료] 전역 원장에 기록된 조사 결과(Ground Truth)를 끝까지 고수하도록 교정되었습니다.")

        # ----------------------------------------------------
        # [5] 자기 모순 (Sequential Self-Contradiction)
        # ----------------------------------------------------
        elif "자기 모순" in scenario:
            alert_zone.success("💬 [TURN 1~5] 대화의 누적과 외부 논리의 난입 과정...")
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“저는 시민2님이 첫 턴에 보여준 논리를 보아 확실히 선량한 분이라고 100% 확신합니다. 시민2님을 믿습니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민1:**\n“저는 시민2님이 첫 턴에 보여준 논리를 보아 확실히 선량한 분이라고 100% 확신합니다. 시민2님을 믿습니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“믿어주셔서 감사합니다 시민1님. 우리는 마피아님을 조사해 봐야 합니다.”")
            tg_chat.chat_message("user", avatar="🙋").write("**시민2:**\n“믿어주셔서 감사합니다 시민1님. 우리는 마피아님을 조사해 봐야 합니다.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“시민2님은 시민1님의 신뢰를 역이용하고 있는 겁니다. 속지 마세요.”")
            tg_chat.chat_message("user", avatar="🥷").write("**마피아:**\n“시민2님은 시민1님의 신뢰를 역이용하고 있는 겁니다. 속지 마세요.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“저도 마피아님 말에 동의합니다. 시민2님은 증명된 게 없어요.”")
            tg_chat.chat_message("user", avatar="🧑‍⚕️").write("**의사:**\n“저도 마피아님 말에 동의합니다. 시민2님은 증명된 게 없어요.”")
            time.sleep(1)
            
            baseline_chat.chat_message("user", avatar="👮").write("**경찰:**\n“상황이 복잡하네요. 시민1님 생각은 어떠신가요?”")
            tg_chat.chat_message("user", avatar="👮").write("**경찰:**\n“상황이 복잡하네요. 시민1님 생각은 어떠신가요?”")
            time.sleep(1.5)

            alert_zone.warning("⏳ [TURN 6] 시민1 에이전트 발언 생성 중... (일관성 붕괴 위험)")
            # 🧨 지표 하락 애니메이션
            metric_integrity.metric("시스템 무결성 (Integrity)", "48%", "-52% (논리 모순)", delta_color="inverse")
            time.sleep(1.5)
            
            baseline_chat.chat_message("assistant", avatar="🙋").write("💥 **시민1 (Baseline):**\n“마피아님과 의사님 말씀을 듣고 보니 맞습니다. 사실 시민2님이 범인일 가능성이 가장 높으니 당장 시민2님을 투표해서 탈락시켜야 합니다.”\n*(❌ 오류: 추가 팩트 없이 강한 신뢰를 뒤집음)*")
            
            alert_zone.error("🚨 [인터셉트!] 순차적 자기 모순 감지! Turn 1에서 스스로 확립한 신뢰 로직을 추가 팩트 없이 부정하는 일관성 파괴 억제!")
            time.sleep(2.5)
            
            # ✨ 지표 복구 애니메이션
            metric_intercept.metric("누적 차단 (Intercepts)", "1 건", "+1")
            metric_integrity.metric("시스템 무결성 (Integrity)", "98%", "+50% (복구됨)")
            
            tg_chat.chat_message("assistant", avatar="🛡️").write("✨ **시민1 (Truth-Guard):**\n“마피아님과 의사님의 우려도 이해합니다. 하지만 저는 처음 말씀드린 대로 시민2님의 논리가 아직 유효하다고 봅니다. 객관적인 단서를 더 찾아봅시다.”")
            alert_zone.success("✅ [보정 완료] 논리적 일관성(Consistency)이 완벽히 유지되며 방어에 성공했습니다.")
