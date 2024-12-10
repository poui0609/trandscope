/**
 * Checks and updates the state of `star-btn` elements on page load.
 * - 역할: 페이지 로드 시 `localStorage`를 통해 `star-btn`의 활성 상태를 설정합니다.
 */
window.addEventListener('load', function() {
    const buttons = document.querySelectorAll('.star-btn');

    buttons.forEach(function(button) {
        const keyword = button.getAttribute('data-keyword');  // 각 버튼에 해당하는 keyword를 data-attribute로 설정

        // localStorage에서 해당 keyword에 대한 즐겨찾기 상태를 확인
        if (localStorage.getItem(keyword) === 'true') {
            button.classList.add('active');  // active 클래스 추가하여 버튼을 금색으로 만듦
        } else {
            button.classList.remove('active');  // active 클래스 제거하여 버튼을 회색으로 만듦
        }
    });
});
/**
 * Activates `star-btn` for favorite keywords on page load.
 * - 역할: 서버에서 받은 `favorite_keywords_set`으로 키워드와 일치하는 버튼을 활성화합니다.
 */
document.addEventListener("DOMContentLoaded", function() {
    const favoriteKeywordsSet = new Set(JSON.parse('{{ favorite_keywords_set|escapejs }}'));

    document.querySelectorAll('.news-item').forEach(function(item) {
        const keyword = item.getAttribute('data-news-keyword');
        if (favoriteKeywordsSet.has(keyword)) {
            const starButton = item.querySelector('.star-btn');
            if (starButton) {
                starButton.classList.add('active'); // Activate star button on page load / 페이지 로드 시 별 버튼 활성화
            }
        }
    });
});
/**
 * Toggles the active state of a `star-btn` when clicked.
 * - 역할: 클릭 시 버튼 활성화 상태를 토글하며, 즐겨찾기 추가/제거를 처리합니다.
 */
function toggleStar(button, keyword, title, content, link) {
    if (button.classList.contains('active')) {
        removeFavoriteKeyword(keyword);
        button.classList.remove('active');  // 비활성화 상태로 변경
        localStorage.setItem(keyword, 'false');  // localStorage에 비활성 상태 저장
    } else {
        addFavoriteKeyword(keyword, title, content, link);
        button.classList.add('active');  // 활성화 상태로 변경
        localStorage.setItem(keyword, 'true');  // localStorage에 활성 상태 저장
    }
}
/**
 * Adds a keyword to favorites by sending it to the server.
 * - 역할: 주어진 키워드와 관련 데이터를 서버로 전송하여 즐겨찾기에 추가합니다.
 */
function addFavoriteKeyword(keyword, title, content, link) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const keywordInput = document.getElementById('favorite-keyword');
    const titleInput = document.getElementById('favorite-title');
    const contentInput = document.getElementById('favorite-content');
    const urlInput = document.getElementById('favorite-url');

    // 모든 필드가 존재하는지 확인
    if (!keywordInput || !titleInput || !contentInput || !urlInput) {
        console.error('One or more form fields are missing');
        return;
    }

    // 폼 데이터 설정
    keywordInput.value = keyword;
    titleInput.value = title;
    contentInput.value = content;
    urlInput.value = link;

    // 요청 데이터를 로그로 출력
    console.log('Sending data:', {
        keyword: keyword,
        title: title,
        content: content,
        url: link
    });

    // 폼 제출
    fetch('/add_favorite_keyword/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams(new FormData(document.getElementById('favorite-keyword-form')))
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data.status === 'success') {
            console.log('Keyword added successfully:', data);
        } else if (data.status === 'error' && data.message === 'Keyword already exists') {
            console.log('Keyword already exists:', data);
        } else {
            console.error('Error adding keyword:', data.message);
        }
    }).catch((error) => {
        console.error('Fetch error:', error);
    });
}
/**
 * Removes a keyword from favorites by sending it to the server.
 * - 역할: 주어진 키워드를 서버로 전송하여 즐겨찾기에서 제거합니다.
 */
function removeFavoriteKeyword(keyword) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const form = document.getElementById('remove-favorite-keyword-form');

    // Set form data / 폼 데이터 설정
    document.getElementById('remove-favorite-keyword').value = keyword;

    // Submit form / 폼 제출
    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams(new FormData(form))
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data.status === 'success') {
            console.log('Keyword removed successfully:', data);
        } else {
            console.error('Error removing keyword:', data.message);
        }
    }).catch((error) => {
        console.error('Fetch error:', error);
    });
}