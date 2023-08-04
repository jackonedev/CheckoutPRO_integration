import React, { useState } from "react";
import { initMercadoPago } from "@mercadopago/sdk-react";
import InternalProvider from "./components/ContextProvider";
import Payment from "./components/Payment";
import Checkout from "./components/Checkout";
import Footer from "./components/Footer";
import { SpinnerCircular } from "spinners-react";
// import { URL, ACCESS_TOKEN, PUBLIC_KEY } from "./config.js";

initMercadoPago("APP_USR-d6b54237-cca0-490f-900a-59405851aa7b");

function App() {
  const backend_url = "http://localhost:8000";

  const item = {
    quantity: 1,
    price: "10",
    amount: 10,
    description: "Some book",
  };

  const [preferenceId, setPreferenceId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [orderData, setOrderData] = useState(item);

  const handleClick = () => {
    setIsLoading(true);
    fetch(backend_url + "/create_preference", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Authorization: `Bearer ${ACCESS_TOKEN}`,
      },
      body: JSON.stringify(orderData),
    })
      .then((response) => {
        return response.json();
      })
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
    <InternalProvider
      context={{ preferenceId, isLoading, orderData, setOrderData }}
    >
      <main>
        {renderSpinner()}
        <Checkout onClick={handleClick} params={item} />
        <Payment />
      </main>
      <Footer />
    </InternalProvider>
  );
}

export default App;
