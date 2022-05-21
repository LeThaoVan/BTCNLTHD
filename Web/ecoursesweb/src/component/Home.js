import React, { useState, useEffect } from 'react';
import { Container, Row,  Spinner } from 'react-bootstrap';
import { useSearchParams } from 'react-router-dom';
import Api, { endpoints } from '../configs/Api';
import Item from '../layout/Item';

function Home() {
    const [route, setRoute] = useState([])
    const [q] = useSearchParams()

    useEffect(() => {
        const loadRoute = async () => {
            let query = ""

            let cateId = q.get("category_id")
            if (cateId !== null)
                query += `category_id=${cateId}`

            let kw = q.get("kw")
            if (kw !== null)
                if (query === "")
                    query += `kw=${kw}`
                else
                    query += `&kw=${kw}`  
            
            const res = await Api.get(`${endpoints['route']}?${query}`)
            setRoute(res.data.results)
        }

        loadRoute()
    }, [q])

    return (
        <Container>
            <h1 className="text-center text-danger">Điểm đến</h1>
            <div>
                <h6>Chọn điểm đến</h6> 
                
                {route.length == 0 && <Spinner animation="grow" />}
            
                <select>
                    {route.map(c => {
                        return <Item id={c.id} name={c.destination} />
                    })}
                </select>
            </div>
           

        </Container>   
    )
}

export default Home