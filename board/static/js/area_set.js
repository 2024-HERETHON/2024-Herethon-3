document.addEventListener("DOMContentLoaded", function () {
    const siCate = document.getElementById("siCate");
    const guCate = document.getElementById("guCate");
    const dongCate = document.getElementById("dongCate");
    const submitButton = document.querySelector(".submitButton");
    const form = document.getElementById("districtForm");
    const selectedSiInput = document.getElementById("selectedSi");
    const selectedGuInput = document.getElementById("selectedGu");
    const selectedDongInput = document.getElementById("selectedDong");

    let selectedSi = "";
    let selectedGu = "";
    let selectedDong = "";

    const guList = {
        서울: [
            "서울전체",
            "강남구",
            "강동구",
            "강북구",
            "강서구",
            "관악구",
            "광진구",
            "구로구",
            "금천구",
            "노원구",
            "도봉구",
            "동대문구",
            "동작구",
            "마포구",
            "서대문구",
            "서초구",
            "성동구",
            "성북구",
            "송파구",
            "양천구",
            "영등포구",
            "용산구",
            "은평구",
            "종로구",
            "중구",
            "중랑구",
        ],

        // 다른 시도별 구 목록도 필요 시 추가
    };

    const dongList = {
        "서울 전체": ["전체 동"],
        강남구: [
            "개포동",
            "개포1동",
            "개포2동",
            "개포4동",
            "논현동",
            "논현1동",
            "논현2동",
            "대치동",
            "대치1동",
            "대치2동",
            "대치4동",
            "도곡동",
            "도곡1동",
            "도곡2동",
            "삼성동",
            "삼성1동",
            "삼성2동",
            "세곡동",
            "수서동",
            "신사동",
            "압구정동",
        ],
        강동구: [
            "상일동",
            "성내동",
            "성내1동",
            "성내2동",
            "성내3동",
            "암사동",
            "암사1동",
            "암사2동",
            "암사3동",
            "천호동",
            "천호1동",
            "천호2동",
            "천호3동",
        ],
        강북구: [
            "번1동",
            "번2동",
            "번3동",
            "삼각산동",
            "삼양동",
            "송중동",
            "송천동",
            "수유동",
            "수유1동",
            "수유2동",
            "수유3동",
            "우이동",
            "인수동",
        ],
        강서구: ["가양동", "등촌동", "염창동", "화곡동"],
        관악구: ["남현동", "봉천동", "신림동"],
        광진구: ["광장동", "구의동", "군자동", "자양동"],
        구로구: ["개봉동", "고척동", "구로동", "신도림동"],
        금천구: ["가산동", "독산동", "시흥동"],
        노원구: ["공릉동", "상계동", "월계동", "중계동"],
        도봉구: ["도봉동", "방학동", "쌍문동", "창동"],
        동대문구: ["답십리동", "신설동", "용두동", "이문동"],
        동작구: ["노량진동", "사당동", "상도동", "흑석동"],
        마포구: ["공덕동", "망원동", "상암동", "서교동"],
        서대문구: ["남가좌동", "북가좌동", "연희동", "홍은동"],
        서초구: ["반포동", "서초동", "잠원동"],
        성동구: ["금호동", "마장동", "성수동", "행당동"],
        성북구: ["길음동", "돈암동", "동선동", "보문동"],
        송파구: ["가락동", "문정동", "방이동", "잠실동"],
        양천구: ["목동", "신월동", "신정동"],
        영등포구: ["당산동", "대림동", "여의도동"],
        용산구: ["남영동", "용문동", "이촌동", "한남동"],
        은평구: ["구산동", "녹번동", "불광동", "역촌동"],
        종로구: ["가회동", "견지동", "부암동", "창신동"],
        중구: ["명동", "신당동", "을지로동", "황학동"],
        중랑구: ["망우동", "면목동", "묵동", "중화동"],
    };

    siCate.addEventListener("click", function (event) {
        if (event.target.tagName === "BUTTON") {
            // 모든 시 버튼에서 active 클래스 제거
            siCate.querySelectorAll("button").forEach((button) => button.classList.remove("active1"));
            event.target.classList.add("active1");

            // 선택된 시 저장
            selectedSi = event.target.textContent.trim();

            // 구와 동 초기화
            selectedGu = "";
            selectedDong = "";
            guCate.innerHTML = "";
            dongCate.innerHTML = "";

            // 기본적으로 구 목록 표시
            guCate.style.display = "block";

            // 구 목록 업데이트
            const guOptions = guList[selectedSi] || [];
            guCate.innerHTML = guOptions.map((gu) => `<button>${gu}</button>`).join("");
        }
    });

    // 구 버튼 클릭 시 이벤트 처리
    guCate.addEventListener("click", function (event) {
        if (event.target.tagName === "BUTTON") {
            // 모든 구 버튼에서 active 클래스 제거
            guCate.querySelectorAll("button").forEach((button) => button.classList.remove("active2"));
            event.target.classList.add("active2");

            // 선택된 구 저장
            selectedGu = event.target.textContent.trim();

            // 동 초기화
            selectedDong = "";
            dongCate.innerHTML = "";
            dongCate.style.display = "none";

            // 동 목록 업데이트
            const dongOptions = dongList[selectedGu] || [];
            dongCate.style.display = "block";
            dongCate.innerHTML = dongOptions.map((dong) => `<button>${dong}</button>`).join("");
        }
    });

    // 동 버튼 클릭 시 이벤트 처리
    dongCate.addEventListener("click", function (event) {
        if (event.target.tagName === "BUTTON") {
            // 모든 동 버튼에서 active 클래스 제거
            dongCate.querySelectorAll("button").forEach((button) => button.classList.remove("active3"));
            event.target.classList.add("active3");

            // 선택된 동 저장
            selectedDong = event.target.textContent.trim();
        }
    });

    submitButton.addEventListener("click", function () {
        selectedSiInput.value = selectedSi;
        selectedGuInput.value = selectedGu;
        selectedDongInput.value = selectedDong;
        form.submit();
    });
});
