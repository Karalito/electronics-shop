import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux'
import { Link } from "react-router-dom";
import { Row, Col, Image, ListGroup, Button, Card } from "react-bootstrap";
import {listProductDetails} from '../actions/productActions'
import Loader from '../components/Loader'
import Message from '../components/Message'


function ProductScreen({ match }) {
  const dispatch = useDispatch()
  const productDetails = useSelector(state => state.productDetails)
  const {loading, error, product} = productDetails
  useEffect(() => {
    dispatch(listProductDetails(match.params.id))
  }, [dispatch, match]);

  return (
    <div>
      <Link to="/" className="btn btn-light my-3">
        Go Back
      </Link>
      {loading ? 
        <Loader/>
        : error
          ? <Message variant='danger'>{error}</Message>
        : (
            <><Row>
              <Col md={6} className="col-product-image">
                <Image src={product.image} alt={product.name} fluid />
              </Col>
              <Col md={3}>
                <ListGroup variant="flush">
                  <ListGroup.Item>
                    <h3>{product.name}</h3>
                    Price: {product.price}€
                  </ListGroup.Item>

                  <ListGroup.Item>Description: {product.description}</ListGroup.Item>

                  <ListGroup.Item>
                    <Row>
                      <Col>Status:</Col>
                      <Col>
                        {product.countInStock > 0 ? "In Stock" : "Out of Stock"}
                      </Col>
                    </Row>
                  </ListGroup.Item>

                  <ListGroup.Item>
                    <Row>
                      <Col>
                        <Button
                          className="btn-block"
                          disabled={product.countInStock == 0}
                          type="button"
                        >
                          Add to Cart
                        </Button>
                      </Col>

                      <Col>
                        <Button
                          className="btn-block"
                          disabled={product.countInStock == 0}
                          type="button"
                        >
                          Add to Wish List
                        </Button>
                      </Col>
                    </Row>
                  </ListGroup.Item>
                </ListGroup>
              </Col>
            </Row><Row>
                <h3>Parameters</h3>
                <Col md={3}>
                  {product.parameters_id}
                </Col>
              </Row></>
          )    
      }
    </div>
  );
}

export default ProductScreen;
