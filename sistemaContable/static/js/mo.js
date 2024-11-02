function actualizar(action) {
    var form = document.getElementById("tabla_empleados");
    form.action = action;
    form.attributes.getNamedItem("method") = "get";
}