const status = sessionStorage.getItem("status")
const element = document.getElementById("disturbances-image")

if (status !== "Выполнено") {
    const container = document.querySelector('.image-container')
    container.innerHTML = `
        <div class="no-data-message">
            <h3>График возмущений не доступен</h3>
            <p>Выполните расчеты на странице "Параметры" чтобы увидеть график</p>
        </div>
    `
} else {
    element.style.visibility = "visible"
}