import React, { useState, useEffect, useContext } from 'react'
import { Container, Col, Badge, Spinner, Row, Image, Button, ListGroup, Form } from 'react-bootstrap'
import { useParams } from 'react-router-dom'
import Api, { endpoints, authAxios } from '../configs/Api'
import { UserContext } from '../App'
import Rating from 'react-rating'
import Moment from 'react-moment'

const BusesDetail = () => {
    const [buses, setBuses] = useState(null)
    const [comments, setComments] = useState([])
    const { busesId } = useParams()
    const [user] = useContext(UserContext)
    

    useEffect(() => {
        const loadBuses = async () => {
            let res = null;
            if (user != null) {
                res = await authAxios().get(endpoints['buses-detail'](busesId))
            } else {
                res = await Api.get(endpoints['buses-detail'](busesId))
            }
            console.info(res.data)
            setBuses(res.data)
        }

        loadBuses()
    }, [])

    useEffect(() => {
        const loadComments = async () => {
            const res = await Api.get(endpoints['buses-comments'](busesId))
            setComments(res.data)
        }

        loadComments()
    }, [comments])

    const like = async () => {
        const res = await authAxios().post(endpoints['like-buses'](busesId))
        setBuses(res.data)
    }

    const rate = async (r) => {
        const res = await authAxios().post(endpoints['rate-buses'](busesId), {
            'rate': r
        })
        console.info(res.data)
        setBuses(res.data)
    }

    if (buses === null)
        return <Container><Spinner animation="grow" /></Container>

    return (
        <Container>
            <h1 className="text-center text-info">CHI TIET CHUYEN XE({busesId})</h1>
            <Row>
                <Col md={5} xs={12}>
                    <Image src={buses.image} fluid />
                </Col>
                <Col md={7} xs={12}>
                    <h2>{buses.name}</h2>
                    {buses.tags.map(t => <Badge key={t.id} bg="info">{t.name}</Badge>)}

                    <div>
                        {user != null && <Button variant={buses.like == true?'primary':'outline-primary'} onClick={like}>Like</Button>}
                        <br></br>
                        {user != null && <Rating initialRating={buses.rating} onClick={rate} />}
                    </div>
                </Col>
            </Row>
            <Row>
                <Col>
                    <div dangerouslySetInnerHTML={{__html: buses.content}}></div>
                </Col>
            </Row>
            <Row>
                <Col>
                    {user != null && <CommentForm busesId={busesId} comments={comments} setComments={setComments} />}
                    <ListGroup>
                        {comments.map(c => <ListGroup.Item>
                            <Image src={c.user.avatar_view} fluid width="50" roundedCircle /> {c.content} - <Moment fromNow>{c.created_date}</Moment>
                        </ListGroup.Item>)}
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    )
}

const CommentForm = ({ lessonId, comments, setComments }) => {
    const [content, setContent] = useState()
    const [user] = useContext(UserContext)

    const addComment = async (event) => {
        event.preventDefault()

        const res = await authAxios().post(endpoints['comments'], {
            'content': content, 
            'lesson': lessonId,
            'user': user.id
        })

        setComments([...comments, res.data])
    }

    return (
        <Form onSubmit={addComment}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Control type="text" value={content} onChange={(evt) => setContent(evt.target.value)} placeholder="Nhap binh luan" />
            </Form.Group>
        
            <Button variant="primary" type="submit">
                Them binh luan
            </Button>
        </Form>
    )
}

export default BusesDetail