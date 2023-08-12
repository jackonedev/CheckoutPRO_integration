function FormCliente({
  formData,
  setFormData,
}) {
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  return (
    <section
      style={{ marginLeft: "20px", flexDirection: "column", display: "flex" }}
    >
      <form>
        <label className="m-2">
          Nombre y apellido:
          <input
            type="text"
            name="nombre_apellido"
            required
            className="ml-2 rounded-sm border-2 border-black"
            value={formData.nombre_apellido}
            onChange={handleChange}
          />
        </label>

        <label className="m-2">
          Email:
          <input
            type="text"
            name="email"
            required
            className="ml-2 rounded-sm border-2 border-black"
            value={formData.email}
            onChange={handleChange}
          />
        </label>

        <label className="m-2">
          Teléfono:
          <input
            type="text"
            name="telefono"
            required
            className="ml-2 rounded-sm border-2 border-black"
            value={formData.telefono}
            onChange={handleChange}
          />
        </label>

        <label className="m-2">
          Dirección:
          <input
            type="text"
            name="direccion"
            required
            className="ml-2 rounded-sm border-2 border-black"
            value={formData.direccion}
            onChange={handleChange}
          />
        </label>

        <label className="m-2">
          Codigo Postal:
          <input
            type="text"
            name="codigo_postal"
            required
            className="ml-2 rounded-sm border-2 border-black"
            value={formData.codigo_postal}
            onChange={handleChange}
          />
        </label>
      </form>
    </section>
  );
}

export default FormCliente;
