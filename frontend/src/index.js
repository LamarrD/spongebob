import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "./custom.scss";
// import "bootstrap/dist/css/bootstrap.min.css";
import Home from "./Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Characters from "./Characters";
import Navbar from "./Navbar";

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/characters" element={<Characters />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);
