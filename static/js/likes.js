async function toggleLike(postId) {
    try {
        const response = await fetch(
            `/api/like/${postId}`,
            {
                credentials: "same-origin",
                method: "UPDATE",
            }
        )
        const data = await response.json();
        if (data.success) {
            const icon = document.querySelector(".like-icon")
            const count = document.querySelector(".like-count")

            count.textContent = data.likes_count
            if (data.user_liked) {
                icon.classList.replace("fa-regular", "fa-solid")
                icon.style.color = "#e25555"
            } else {
                icon.classList.replace("fa-solid", "fa-regular")
                icon.style.color = "#3b3b3b"
            }
        }
    } catch (error) {
        console.log(error);
    }
}

async function loadLikeState(postId, button) {
    try {
        const response = await fetch(`/api/like/${postId}`, {
            credentials: "same-origin",
        })
        const data = await response.json();
        if (data.success && data.has_liked) {
            const icon = button.querySelector('.like-icon');
            icon.classList.replace('fa-regular', 'fa-solid');
            icon.style.color = '#f56565';
        }
    } catch (error) {
        console.log("Ошибка загрузки: ", error)
    }
}

// DOM — Document Object Model

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn__btn").forEach(button => {
        const postId = button.dataset.postId;
        loadLikeState(postId, button);
        button.addEventListener("click", () => toggleLike(postId))
    })
})