import React, { useState, useEffect } from 'react'
import { Form, Button, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import Message from '../components/Message'
import CheckoutSteps from '../components/CheckoutSteps'

function PlaceOrderScreen() {
  const cart = useSelector((state) => state.cart)
  cart.itemsPrice = cart.cartItems.reduce((acc, item) => acc + item.price * item.qty,0).toFixed(2)
  cart.shippingPrice = (cart.itemsPrice >= 100 ? 0 : 8.50).toFixed(2)
  cart.totalPrice = (Number(cart.itemsPrice) + Number(cart.shippingPrice)).toFixed(2)
  const placeOrder = () => {
      console.log('place order')
  }
  return (
    <div>
      <CheckoutSteps step1 step2 step3 step4 />
      <Row>
        <Col md={8}>
          <ListGroup variant='flush'>
            <ListGroup.Item>
              <h2>Order Items</h2>
              {cart.cartItems.lenght === 0 ? (
                <Message variant='info'>Your Cart is empty !</Message>
              ) : (
                <ListGroup variant='flush'>
                  {cart.cartItems.map((item, index) => (
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
                <h3>Shipping To</h3>
                <p>
                  <strong>Country:</strong>
                  {cart.shippingAddress.country}
                </p>
                <p>
                  <strong>City:</strong>
                  {cart.shippingAddress.city}
                </p>
                <p>
                  <strong>Address:</strong>

                  {cart.shippingAddress.address}
                </p>
                <p>
                  <strong>Postal Code:</strong>
                  {cart.shippingAddress.postalCode}
                </p>

                <p>
                  <strong>Payment Method:</strong>
                  {cart.paymentMethod}
                </p>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Items:</Col>
                  <Col>{cart.itemsPrice}€</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Shipping:</Col>
                  <Col>{cart.shippingPrice}€</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Total:</Col>
                  <Col>{cart.totalPrice}€</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Button
                type='button'
                className='btn-block'
                disabled={cart.cartItems === 0}
                onClick={placeOrder}>Place Order</Button>
              </ListGroup.Item>
            </ListGroup>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default PlaceOrderScreen
