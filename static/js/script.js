
const input = document.getElementById("status-input")
input.value = sessionStorage.getItem("status") || ""

function random() {
    return Math.round(((Math.random() * 0.7 + 0.01) + Number.EPSILON) * 100) / 100
}

if (input.value !== "Выполнено") {
    refill()
}
else {
 
    for (let i=1; i<10; i++) {
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("faks-" + i + "-" + j) || ""
            }
        }
    }


    for (let i=1; i<13; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) {
            el.value = sessionStorage.getItem("init-eq-" + i) || ""
        }
    }


    for (let i=1; i<30; i++) {
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("equations-" + i + "-" + j) || ""
            }
        }
    }
}

function getFaks() {
    const faks = []
    for (let i=1; i<10; i++) {
        const temp = []
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) temp.push(el.value)
        }
        faks.push(temp)
    }
    return faks
}

function getInitialEquations() {
    const init_eq = []
    for (let i=1; i<13; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) init_eq.push(el.value)
    }
    return init_eq
}

function getRestrictions() {
    const restrictions = []
    for (let i=1; i<13; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) restrictions.push(el.value)
    }
    return restrictions
}

function getEquations() {
    const equations = []
    for (let i=1; i<30; i++) {
        const temp = []
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) temp.push(el.value)
        }
        equations.push(temp)
    }
    return equations
}

async function process() {
    const faks = getFaks()
    const init_eq = getInitialEquations()
    const restrictions = getRestrictions()
    const equations = getEquations()

    const response = await fetch('/draw_graphics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "faks": faks,
            "initial_equations": init_eq,
            "restrictions": restrictions,
            "equations": equations
        })
    })

    const result = await response.json()
    input.value = result.status
    sessionStorage.setItem("status", result.status)
}

function refill() {
  
    for (let i=1; i<10; i++) {
        for (let j=1; j<5; j++) {
            let value = random()
            sessionStorage.setItem("faks-" + i + "-" + j, value)
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) el.value = value
        }
    }

    for (let i=1; i<13; i++) {
        let value = random()
        sessionStorage.setItem("init-eq-" + i, value)
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = value
    }


    for (let i=1; i<30; i++) {
        for (let j=1; j<6; j++) {
            let value = random()
            sessionStorage.setItem("equations-" + i + "-" + j, value)
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) el.value = value
        }
    }
    
    sessionStorage.removeItem("status")
    input.value = ""
}