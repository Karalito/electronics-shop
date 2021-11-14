import React, { useState, useEffect } from 'react'
import { Form, Button, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { PayPalButton } from 'react-paypal-button-v2'
import Message from '../components/Message'
import Loader from '../components/Loader'

import { getOrderDetails, payOrder } from '../actions/orderActions'
import { ORDER_PAY_RESET } from '../constants/orderConstants'

function UserOrdersScreen({ match }) {
  const orderId = match.params.id
  const dispatch = useDispatch()

  const [sdkReady, setSdkReady] = useState(false)

  const orderDetails = useSelector((state) => state.orderDetails)
  const { order, error, loading } = orderDetails

  const orderPay = useSelector((state) => state.orderPay)
  const { loading: loadingPay, success: successPay } = orderPay

  if (!loading && !error) {
    order.itemsPrice = order.orderItems
      .reduce((acc, item) => acc + item.price * item.qty, 0)
      .toFixed(2)
  }

  const addPaypalScript = () => {
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src =
      'https://www.paypal.com/sdk/js?client-id=ActATsD-3AJzGWAl0qUs8MCFGsQChCpvb_ZNu9qie9PKEgWtTCJphpSY4BOI6M8ihWJ9TY9U0Ji_d_dW'
    script.async = true
    script.onload = () => {
      setSdkReady(true)
    }
    document.body.appendChild(script)
  }
  useEffect(() => {
    if (!order || successPay || order._id !== Number(orderId)) {
      dispatch({ type: ORDER_PAY_RESET })
      dispatch(getOrderDetails(orderId))
    } else if (!order.isPaid) {
      if (!window.paypal) {
        addPaypalScript()
      } else {
        setSdkReady(true)
      }
    }
  }, [dispatch, order, orderId, successPay])

  const successPaymentHandler = (paymentResult) => {
    dispatch(payOrder(orderId, paymentResult))
  }

  return loading ? (
    <Loader />
  ) : error ? (
    <Message variant='danger'>{error}</Message>
  ) : (
    <div>
      <Row>
        <Col md={8}>
          <ListGroup variant='flush'>
            <ListGroup.Item>
              <h2>Order Items</h2>
              {order.orderItems.lenght === 0 ? (
                <Message variant='info'>
                  You haven't made any orders yet!
                </Message>
              ) : (
                <ListGroup variant='flush'>
                  {order.orderItems.map((item, index) => (
                    <ListGroup.Item key={index}>
                      <Row>
                        <Col md={1}>
                          <Image
                            src={item.image}
                            alt={item.name}
                            fluid
                            rounded
                          />
                        </Col>
                        <Col>
                          <Link to={`/product/${item.product}`}>
                            {item.name}
                          </Link>
                        </Col>

                        <Col md={4}>
                          {item.qty} X {item.price}€ ={' '}
                          {(item.qty * item.price).toFixed(2)}€
                        </Col>
                      </Row>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </ListGroup.Item>
          </ListGroup>
        </Col>
        <Col md={4}>
          <Card>
            <ListGroup variant='flush'>
              <ListGroup.Item>
                <h2>Order Summary</h2>
              </ListGroup.Item>
              <ListGroup.Item>
                <h4>Shipping Information</h4>
                <p>
                  <strong>
                    {order.user.name} {order.user.surname}
                  </strong>
                </p>
                <p>
                  <strong>
                    <a href={`mailto:${order.user.email}`}>
                      {order.user.email}
                    </a>
                  </strong>
                </p>
                <p>
                  <strong>Country: </strong>
                  {order.shippingAddress.country}
                </p>
                <p>
                  <strong>City: </strong>
                  {order.shippingAddress.city}
                </p>
                <p>
                  <strong>Address: </strong>

                  {order.shippingAddress.address}
                </p>
                <p>
                  <strong>Postal Code: </strong>
                  {order.shippingAddress.postalCode}
                </p>

                <p>
                  <strong>Payment Method: </strong>
                  {order.paymentMethod}
                </p>
                {order.isPaid ? (
                  <Message variant='success'>Paid On {order.paidAt}</Message>
                ) : (
                  <Message variant='warning'>Not Paid</Message>
                )}
                {order.isDelivered ? (
                  <Message variant='success'>
                    Delivered On {order.deliveredAt}
                  </Message>
                ) : (
                  <Message variant='warning'>Not Delivered</Message>
                )}
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Items: </Col>
                  <Col>{order.itemsPrice}€</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Shipping:</Col>
                  <Col>{order.shippingPrice}€</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Total:</Col>
                  <Col>{order.totalPrice}€</Col>
                </Row>
              </ListGroup.Item>
              {!order.isPaid && (
                <ListGroup.Item>
                  {loadingPay && <Loader />}

                  {!sdkReady ? (
                    <Loader />
                  ) : (
                    <PayPalButton
                      amount={order.totalPrice}
                      onSuccess={successPaymentHandler}
                    />
                  )}
                </ListGroup.Item>
              )}
            </ListGroup>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default UserOrdersScreen
