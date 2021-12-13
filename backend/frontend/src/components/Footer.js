import {
  Facebook,
  Instagram,
  Pinterest,
  Twitter,
  YouTube,
  Room,
  Phone,
  MailOutline,
} from '@material-ui/icons'
import styled from 'styled-components'
import { tablet } from '../responsive'

const Container = styled.div`
background-color: #2B2B2B;
color: white;
`
const Wrapper = styled.div`
  display: flex;
  align-items: center;
  width: 80%;
  margin: auto;
  ${tablet({flexDirection: "column"})}
`
// Footer left side styling
const Left = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  ${tablet({textAlign: "center"})}
`
const Logo = styled.h1``
const Description = styled.p`
  margin: 20px 0;
`
const SocialContainer = styled.div`
  display: flex;
  ${tablet({justifyContent: "center"})}
`
const SocialIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
`
// Footer center styling
const Center = styled.div`
  flex: 1;
  padding: 20px;
  ${tablet({display: "none"})}
`
const Title = styled.h3`
  margin-bottom: 30px;
`

const List = styled.ul`
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
`

const ListItem = styled.a`
  width: 50%;
  margin-bottom: 10px;
  color: gray;
  text-decoration: none;
`

// Footer right side styling
const Right = styled.div`
  flex: 1;
  padding: 20px;
`

const ContactItem = styled.div`
  margin-bottom: 20px;
  display: flex;
`

const Line = styled.hr`
  width: 80%;
  margin: auto;
`
// Footer copyright
const Copyright = styled.div`
  margin: auto;
  padding: 20px;
  font-weight: 500;
`

// Function that returns footer container
function Footer() {
  return (
    <Container>
    <Line />  
      <Wrapper>
        <Left>
          <Logo>Amplo.</Logo>
          <Description>
            Some Kind of description about this webpage we sell best products
            etc etc etc
          </Description>
          <SocialContainer>
            <SocialIcon bg='E60023'>
              <YouTube />
            </SocialIcon>
            <SocialIcon bg='E4405F'>
              <Instagram />
            </SocialIcon>
            <SocialIcon bg='3B5999'>
              <Facebook />
            </SocialIcon>
            <SocialIcon bg='55ACEE'>
              <Twitter />
            </SocialIcon>
            <SocialIcon bg='E60023'>
              <Pinterest />
            </SocialIcon>
          </SocialContainer>
        </Left>
        <Center>
          <Title>Help</Title>
          <List>
            <ListItem href='#'>Payment</ListItem>
          </List>
          <List>
            <ListItem href='#'>Delivery</ListItem>
          </List>
          <List>
            <ListItem href='#'>Returns</ListItem>
          </List>
          <List>
            <ListItem href='#'>Guest purchase</ListItem>
          </List>
          <List>
            <ListItem href='#'>Electronic receipt</ListItem>
          </List>
        </Center>
        <Center>
          <Title>About us</Title>
          <List>
            <ListItem href='#'>About Amplo</ListItem>
          </List>
          <List>
            <ListItem href='#'>Privacy policy</ListItem>
          </List>
          <List>
            <ListItem href='#'>Terms and conditions</ListItem>
          </List>
          <List>
            <ListItem href='#'>Cookies policy</ListItem>
          </List>
          <List>
            <ListItem href='#'>Work with us</ListItem>
          </List>
        </Center>
        <Right>
          <Title>Contact us</Title>
          <ContactItem>
            <Room style={{ marginRight: '10px' }} />
            Fictional Street 2. Vilnius
          </ContactItem>
          <ContactItem>
            <Phone style={{ marginRight: '10px' }} />
            +37067104021
          </ContactItem>
          <ContactItem>
            <MailOutline style={{ marginRight: '10px' }} />
            karl.pigaga@gmail.com
          </ContactItem>
        </Right>
      </Wrapper>
      <Line />
      <Wrapper>
        <Copyright> © 2021 Copyright: Karolis Pigaga.</Copyright>
      </Wrapper>
    </Container>
  )
}

export default Footer