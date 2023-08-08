import React, { useState } from "react";
import FormCliente from "../form/FormCliente";
import { Context } from "../ContextProvider";

function FormContainer() {

  const {
    preferenceId,
    isLoading: disabled,
    orderData,
    setOrderData,
    formDataCliente, 
    setFormDataCliente
  } = React.useContext(Context);

  return (
    <center>
      <FormCliente
        formData={formDataCliente}
        setFormData={setFormDataCliente}
      />
    </center>
  );
}

export default FormContainer;
