
const status = sessionStorage.getItem("status")

if (status !== "Выполнено") {
    const grid = document.querySelector('.diagrams-grid')
    grid.innerHTML = `
        <div class="no-data-message" style="grid-column: 1 / -1;">
            <h3>Диаграммы не доступны</h3>
            <p>Выполните расчеты на странице "Параметры" чтобы увидеть диаграммы</p>
        </div>
    `
} else {
    document.getElementById("diagram-image").style.visibility = "visible"
    document.getElementById("diagram2-image").style.visibility = "visible"
    document.getElementById("diagram3-image").style.visibility = "visible"
    document.getElementById("diagram4-image").style.visibility = "visible"
    document.getElementById("diagram5-image").style.visibility = "visible"
}