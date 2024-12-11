
/*userpage로 이동      */
function redirectToUserPage() {
    window.location.href = "/userPage.html";
    }
/* mainpage로 이동    */
function redirectToMainpage() {
    window.location.href = "/page1.html";
}

/* detailpage로 이동   */
function redirectToDatailpage(ranking_id, keyword, title, content, link) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // 최근 키워드 추가
    fetch('/add_recent_keyword/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({
            'keyword': keyword,
            'title': title,
            'content': content,
            'url': link
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data.status === 'success') {
            console.log('Keyword added to recent:', data);
            // page3로 이동
            const url = `/page3/${ranking_id}/`;
            window.location.href = url;
        } else {
            console.error('Error adding to recent:', data.message);
        }
    }).catch((error) => {
        console.error('Fetch error:', error);
    });
}
