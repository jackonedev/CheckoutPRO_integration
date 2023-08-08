import React, { useState } from "react";
import { initMercadoPago } from "@mercadopago/sdk-react";
import InternalProvider from "./components/ContextProvider";
import Payment from "./components/pure/Payment";
import Checkout from "./components/pure/Checkout";
import Footer from "./components/pure/Footer";
import { SpinnerCircular } from "spinners-react";
import FormContainer from "./components/container/FormContainer";

initMercadoPago("APP_USR-ff96fe80-6866-4888-847e-c69250754d38");

function OrderHandling({ sendData, setPreferenceId }) {
  const PORT = 8000;
  const HOST = "localhost";
  const URL = `http://${HOST}:${PORT}`;

  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    console.log("sendData: ", sendData);
    setIsLoading(true);
    fetch(URL + "/v1/create_preference", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendData),
    })
      .then((response) => response.json())
      .then((preference) => {
        setPreferenceId(preference.id);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const renderSpinner = () => {
    if (isLoading) {
      return (
        <div className="spinner-wrapper">
          <SpinnerCircular сolor="#800000" />
        </div>
      );
    }
  };

  return (
    <div>
      {renderSpinner()}
      <Checkout onClick={handleClick} params={sendData.orderData} />
    </div>
  );
}

function App() {
  const item = {
    quantity: 1,
    price: "5000",
    amount: 5000,
    description: "Mobile Phone",
    img_url:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/DynaTAC8000X.jpg/220px-DynaTAC8000X.jpg",
    name: "Motorola DynaTAC 8000X",
  };
  const client = {
    nombre_apellido: "Lalo Landa",
    email: "test_user_36961754@testuser.com",
    telefono: "3516475847",
    direccion: "calle falsa 123",
    codigo_postal: "5000",
  };

  const [preferenceId, setPreferenceId] = useState(null);
  const [orderData, setOrderData] = useState(item);
  const [formDataCliente, setFormDataCliente] = useState(client);

  const combinedData = {
    orderData: orderData,
    formDataCliente: formDataCliente,
  };
  return (
    <InternalProvider
      context={{
        preferenceId,
        orderData,
        setOrderData,
        formDataCliente,
        setFormDataCliente,
      }}
    >
      <main>
        <OrderHandling
          sendData={combinedData}
          setPreferenceId={setPreferenceId}
        />
        <Payment />
        <FormContainer />
      </main>
      <Footer />
    </InternalProvider>
  );
}

export default App;
