const socket = io();
const postId = document.getElementById('post-id')?.value;
const currentUserId = document.getElementById('current-user-id')?.value;
const commentContainer = document.getElementById('comments-container');
const commentForm = document.getElementById('comment-form');

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString.endsWith('Z') ? dateString : dateString + 'Z');

    if (isNaN(date.getTime())) return "недавно";

    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return "только что";

    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} мин. назад`;
    }

    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} ч. назад`;
    }

    return date.toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function addCommentToDOM(comment) {
    const commentElement = document.createElement('div');
    commentElement.className = 'comment';
    commentElement.id = `comment-${comment.id}`; // Добавляем ID для удобного удаления

    const isOwner = currentUserId && String(currentUserId) === String(comment.author_id);
    // JS       : `text: ${data}`
    // Python   : f"text: {data}"
    // ИСПРАВЛЕНО: корректные кавычки в onclick
    const deleteBtn = isOwner
        ? `<button class="delete-btn" onclick="deleteComment(${comment.id})">Удалить</button>`
        : "";

    commentElement.innerHTML = `
        <div class="comment-header">
            <div class="comment-author">
                <strong><a href="/profile/${comment.author_id}">${escapeHtml(comment.author_name)}</a></strong>
            </div>
            <div class="comment-meta">
                <span class="comment-date">${formatDate(comment.created_at)}</span>
            </div>
            <div class="comment-content">
                ${escapeHtml(comment.content)}
            </div>
            ${deleteBtn}
        </div>
    `;
    return commentElement;
}

// --- СОБЫТИЯ ---

if (postId) {
    socket.emit("join_post", { post_id: parseInt(postId) });
}

// Загрузка существующих комментариев
socket.on("initial_comments", (data) => {
    if (!commentContainer) return;

    const comments = data.comments;
    commentContainer.innerHTML = "";

    if (comments.length < 1) {
        commentContainer.innerHTML = '<h2 id="no-comments">Комментариев пока нет</h2>';
    } else {
        comments.forEach(comment => {
            commentContainer.appendChild(addCommentToDOM(comment));
        });
    }
});

// Слушаем появление НОВОГО комментария
socket.on("new_comment", (comment) => {
    const noCommentsMsg = document.getElementById('no-comments');
    if (noCommentsMsg) noCommentsMsg.remove();

    // Добавляем в начало списка (самые свежие сверху)
    commentContainer.prepend(addCommentToDOM(comment));
});

// Отправка комментария
if (commentForm) {
    commentForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const input = document.getElementById("comment-input");
        const content = input.value.trim();

        if (content && postId) {
            socket.emit("add_comment", {
                post_id: parseInt(postId),
                content: content
            });
            input.value = "";
        }
    });
}

// Функция удаления для кнопки
window.deleteComment = function(commentId) {
    if (confirm("Удалить комментарий?")) {
        socket.emit("delete_comment", { comment_id: commentId });
    }
};

// Слушаем событие удаления от сервера
socket.on("comment_deleted", (data) => {
    const el = document.getElementById(`comment-${data.comment_id}`);
    if (el) el.remove();
});