import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Spinner, Row } from 'react-bootstrap';
import Api, { endpoints } from '../configs/Api';
import Item from '../layout/Item';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

function Buses() {
    const [buses, setBuses] = useState([])
    const { routeId } = useParams()

    useEffect(() => {
        const loadBuses = async () => {
            const res = await Api.get(endpoints['buses'](routeId))
            setBuses(res.data)

            console.info(res.data)
        }

        loadBuses()
    }, [])

    return (
        <Container>
            <h1 className="text-center text-info">Danh sách chuyến xe của tuyến xe (ROUTE: {routeId}) </h1>
            
            {buses.length == 0 && <Spinner animation="grow" />}
            
            <Row>
                {buses.map(c => {
                    return <Item id={c.id} image={c.image} name={c.namet} isBuses={true} />
                })}
            </Row>
        </Container>
    )
}

export default Buses