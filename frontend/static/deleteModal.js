function deleteModal(id_company, id_owner){

    document.getElementById("id_company").value = id_company
    document.getElementById("id_owner").value = id_owner
    new bootstrap.Modal(document.getElementById('deleteModal')).show()

}