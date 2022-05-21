import React, { memo } from 'react'
import { Col, Card, Button } from "react-bootstrap"
import { useNavigate } from "react-router-dom"

const Item = (props) => {
    const nav = useNavigate()

    const goToBuses = () => {
        if (props.isBuses === true)
            nav(`/buses/${props.id}`)
        else
            nav(`/route/${props.id}/buses`)
    }

    let btnDetail = "Xem cac chuyen xe"
    if (props.isBuses === true)
        btnDetail = "Xem chi tiet"

    return (
        <Col md={4} xs={12}>
            <Card>
                <Card.Img variant="top" src={props.image} />
                <Card.Body>
                    <Card.Title>{props.subject}</Card.Title>
                    <Button variant="primary" onClick={goToBuses}>{btnDetail}</Button>
                </Card.Body>
            </Card>
        </Col>
    )
}

export default memo(Item)