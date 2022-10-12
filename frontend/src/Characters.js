import React from "react";
import { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Card, Button } from "react-bootstrap";
import { HandThumbsUp, HandThumbsDown } from "react-bootstrap-icons";

function About() {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    // call api gateway to get characters
    fetch(`${process.env.REACT_APP_API}/characters`)
      .then((results) => results.json())
      .then((data) => {
        console.log(data);
        setCharacters(data);
      });
  }, []);

  const characterCards = characters.map((character) => {
    return (
      <Col xs={12} md={6} lg={4} className="mb-4">
        <Card style={{ width: "18rem" }}>
          <Card.Img variant="top" src={`/img/${character.id}.webp`} />
          <Card.Body>
            <Card.Title>{character.full_name}</Card.Title>
            <Card.Text>{character.species}</Card.Text>
            <Button variant="primary">
              <HandThumbsUp />
              {character.likes}
            </Button>
            <Button variant="secondary">
              <HandThumbsDown />
              {character.dislikes}
            </Button>
          </Card.Body>
        </Card>
      </Col>
    );
  });
  return (
    <Container id="about" fluid={true}>
      <Row>{characterCards}</Row>
    </Container>
  );
}

export default About;
