/**
 * Toggles the `active` class for a clicked `.keyword-section`.
 * - 역할: 모든 `.keyword-section`에서 `active` 클래스를 제거하고, 클릭된 요소에만 추가.
 */
function toggleSection(element) {
    // 모든 .keyword-section에서 active 클래스를 제거
    const sections = document.querySelectorAll('.keyword-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // 클릭한 요소에만 active 클래스를 추가
    element.classList.add('active');
}

/**
 * Sends keyword data to the server and redirects to the article.
 * - 역할: 서버에 키워드를 저장하고 성공 시 `url`로 이동.
 */
function viewArticle(url, keyword, title, content) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('{% url "add_recent_keyword" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({
                'keyword': keyword,
                'title': title,
                'content': content,
                'url': url
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            if (data.status === 'success') {
                console.log('Keyword added to recent:', data);
                window.location.href = url;  // URL로 이동
            } else {
                console.error('Error adding to recent:', data.message);
            }
        }).catch((error) => {
            console.error('Fetch error:', error);
        });
    }

/**
 * Toggles the visibility of the signup form.
 * - 역할: `signup-form`을 표시하거나 숨기고, 동시에 `login-form`을 숨깁니다.
 */
function toggleSignup() {
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');
    if (signupForm.style.display === 'none' || signupForm.style.display === '') {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
    } else {
        signupForm.style.display = 'none';
    }
}
/**
 * Toggles the visibility of the login form.
 * - 역할: `login-form`을 표시하거나 숨기고, 동시에 `signup-form`을 숨깁니다.
 */
function toggleLogin() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    if (loginForm.style.display === 'none' || loginForm.style.display === '') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
    }
}
/**
 * Toggles the visibility of a specific text element.
 * - 역할: 주어진 `elementId`의 텍스트를 표시하거나 숨기고, 다른 `.hidden-text` 요소는 숨김.
 */
function showText(elementId) {
    const element = document.getElementById(elementId);
    if (element.classList.contains('visible')) {
        element.classList.remove('visible');
    } else {
        document.querySelectorAll('.hidden-text').forEach(text => {
            text.classList.remove('visible');
        });
        element.classList.add('visible');
    }
}
/**
 * Ensures the favorite text is visible on page load.
 * - 역할: 페이지 로드 시 `#favorite-text`에 `visible` 클래스를 추가.
 */
document.addEventListener("DOMContentLoaded", function() {
    const favoriteText = document.getElementById('favorite-text');
    favoriteText.classList.add('visible');
});
/**
 * Toggles the `active` state of a `star-btn` and updates localStorage.
 * - 역할: 버튼 활성화 상태를 토글하며, 즐겨찾기 추가/제거를 처리.
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