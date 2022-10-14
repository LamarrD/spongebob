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

  function changeLikes(id, change)  {
    fetch(`${process.env.REACT_APP_API}/character/${id}?${change}=true`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", },
    })
      .then((results) => results.json())
      .then((data) => {
        setCharacters(
          characters.map((character) => {
            if (character.id === data.id) { 
              character.likes = data.likes 
            }
            return character;
          })
        );
      });
  };

  function getRandomFact(id)  {
    fetch(`${process.env.REACT_APP_API}/character/${id}/fact`)
      .then((results) => results.text())
      .then((data) => {
        console.log(data)
      });
  };


  const characterCards = characters.map((character) => {
    return (
      <Col xs={12} md={6} lg={4} className="mb-4">
        <Card style={{ width: "18rem" }}>
          <Card.Img variant="top" src={`/img/${character.id}.webp`} />
          <Card.Body>
            <Card.Title>{character.full_name}</Card.Title>
            <Card.Text>{character.species}</Card.Text>
            <Button value={character.id} variant="secondary" onClick={() => changeLikes(character.id, "decrement")}>
              <HandThumbsDown />
            </Button>
              {character.likes}
            <Button value={character.id} variant="primary" onClick={() => changeLikes(character.id, "increment")}>
              <HandThumbsUp />
            </Button>
            <Button onClick={()=> getRandomFact(character.id)}>
              Get Random Fact
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
