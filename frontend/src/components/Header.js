import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Nav, Navbar, Container, NavDropdown } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { logout } from '../actions/userActions'

function Header() {
  const userLogin = useSelector((state) => state.userLogin)
  const { userInfo } = userLogin

  const dispatch = useDispatch()

  const logoutHandler = () => {
    dispatch(logout())
  }
  
  return (
    <header>
      <Navbar bg='dark' variant='dark' expand='lg' collapseOnSelect>
        <Container>
          <LinkContainer to='/'>
            <Navbar.Brand>Amplo</Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls='basic-navbar-nav' />
          <Navbar.Collapse id='basic-navbar-nav'>
            <Nav
              className='me-auto my-2 my-lg-0'
              style={{ maxHeight: '100px' }}
              navbarScroll
            >
              {userInfo ? (
                <NavDropdown title={userInfo.name} id='username'>
                  <LinkContainer to='/profile'>
                    <NavDropdown.Item>Profile</NavDropdown.Item>
                  </LinkContainer>
                  <NavDropdown.Item onClick={logoutHandler}>
                    Logout
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                <LinkContainer to='/login'>
                  <Nav.Link href='/login'>
                    <i className='far fa-user'></i>Login
                  </Nav.Link>
                </LinkContainer>
              )}

              <LinkContainer to='/cart'>
                <Nav.Link href='/cart'>
                  <i className='fas fa-shopping-cart'></i>Cart
                </Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  )
}

export default Header
