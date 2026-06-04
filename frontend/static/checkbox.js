function vincularCheckbox(checkboxId, inputId){

    const checkbox = document.getElementById(checkboxId)
    const input = document.getElementById(inputId)

    checkbox.addEventListener("change", () => {
            input.disabled = !checkbox.checked;
    })

}

function valorCheckboxes(checkboxId, inputId) {

    const checkbox = document.getElementById(checkboxId)
    const input = document.getElementById(inputId)

    checkbox.addEventListener("change", () => {

        if(checkbox.checked){checkbox.value = true}
        else{
            checkbox.value = false
            input.value = 0
        }

    })

}

vincularCheckbox("piscina", "cantidadPiscina")
vincularCheckbox("ringbox", "numRingBox")
valorCheckboxes("piscina", "cantidadPiscina")
valorCheckboxes("ringbox", "numRingBox")