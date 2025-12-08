async function toggleLike(postId) {
    try {
        const response = await fetch(
            `/api/like/${postId}`,
            {
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