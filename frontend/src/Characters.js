import React from "react";
import { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Card, Button, Modal } from "react-bootstrap";
import { HandThumbsUp, HandThumbsDown } from "react-bootstrap-icons";
import Spinner from "react-bootstrap/Spinner";

function About() {
  const [characters, setCharacters] = useState([]);
  const [show, setShow] = useState(false);
  const [fact, setFact] = useState("");

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useEffect(() => {
    // call api gateway to get characters
    fetch(`${process.env.REACT_APP_API}/characters`)
      .then((results) => results.json())
      .then((data) => {
        console.log(data);
        setCharacters(data);
      });
  }, []);

  function changeLikes(id, change) {
    fetch(`${process.env.REACT_APP_API}/character/${id}?${change}=true`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
    })
      .then((results) => results.json())
      .then((data) => {
        setCharacters(
          characters.map((character) => {
            if (character.id === data.id) {
              character.likes = data.likes;
            }
            return character;
          })
        );
      });
  }

  function getRandomFact(character) {
    setFact(
      <div className="d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
    setShow(true);

    fetch(`${process.env.REACT_APP_API}/character/${character.id}/fact`)
      .then((results) => results.text())
      .then((data) => {
        console.log(data);
        setFact(data);
      });
  }

  const characterCards = characters.map((character) => {
    return (
      <Col xs={12} md={6} lg={4} className="mb-4">
        <Card style={{ width: "18rem" }}>
          <Card.Img variant="top" src={`/img/${character.id}.webp`} />
          <Card.Body>
            <Card.Title>{character.full_name}</Card.Title>
            <Card.Text>{character.species}</Card.Text>
            <div className="d-flex justify-content-center">
              <Button
                className="m-1"
                value={character.id}
                variant="secondary"
                onClick={() => changeLikes(character.id, "decrement")}
              >
                <HandThumbsDown />
              </Button>
              <span className="my-auto"> {character.likes} </span>
              <Button
                className="m-1"
                value={character.id}
                variant="primary"
                onClick={() => changeLikes(character.id, "increment")}
              >
                <HandThumbsUp />
              </Button>
            </div>
            <div className="d-flex justify-content-center">
              <Button onClick={() => getRandomFact(character)}>Get Random Fact</Button>
            </div>
          </Card.Body>
        </Card>
      </Col>
    );
  });
  return (
    <Container id="about" fluid={true}>
      <Row>{characterCards}</Row>
      <Modal show={show} onHide={handleClose} aria-labelledby="contained-modal-title-vcenter" centered>
        <Modal.Header closeButton>
          <Modal.Title>Random Fact</Modal.Title>
        </Modal.Header>
        <Modal.Body>{fact}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

export default About;
