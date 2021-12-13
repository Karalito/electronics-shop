import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

function SearchBox() {
  const [keyword, setKeyword] = useState('')

  let history = useHistory()

  const submitHandler = (e) => {
    e.preventDefault()
    if (keyword) {
      history.push(`/?keyword=${keyword}&page=1`)
    } else {
      history.push(history.push(history.location.pathname))
    }
  }

  return (
    <Form
      onSubmit={submitHandler}
      className='d-flex'
      style={{ marginRight: '1rem', alignItems: 'center' }}
    >
      <Form.Control
        type='text'
        name='q'
        placeholder='Search'
        onChange={(e) => setKeyword(e.target.value)}
        className='mr-sm-2 ml-sm-5'
        style={{height: '80%'}}
      ></Form.Control>

      <Button type='submit' variant='success'
      style={{margin: '0 0.5rem',height: '80%', lineHeight: '0'}}>
        Search
      </Button>
    </Form>
  )
}

export default SearchBox
