import React from "react";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { useLocation } from "react-router-dom";

export default function CustomNavbar() {
  const location = useLocation();

  return (
    <Navbar expand="lg" className="navbar mb-3 p-3 bg-primary text-dark" style={{}}>
      <Container fluid={true}>
        <Navbar.Brand href="/" className="">
          <img data-qa="logo" height="50" alt="" src="/img/spongebob_logo.png" className="sticky"></img>
        </Navbar.Brand>
        <div className=""></div>
        <div>
          <Navbar.Toggle aria-controls="navbar" />
          <Navbar.Collapse id="navbar">
            <Nav activeKey={location.pathname}>
              <Nav.Link id="characters" href="/characters">
                Characters
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </div>
      </Container>
    </Navbar>
  );
}
