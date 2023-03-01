import type { NextPage } from 'next'
import Head from 'next/head'
import {
  Input,
  Button,
  Box,
  Container,
  Text,
  useToast,
  Textarea
} from '@chakra-ui/react'
import Layout from '../components/layout'
import { CheckRes } from '../lib/dateFormat'
import React, { useState } from 'react'

const Admin: NextPage = () => {

  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const toast = useToast()

  const submitForm = async (e : React.SyntheticEvent) => {
    e.preventDefault()
    let res = await fetch(process.env.NEXT_PUBLIC_API_LEAD + "/send", {
      method: "POST",
      body: JSON.stringify({ password, message })
    })
    let data : CheckRes = await res.json()
    console.log(data)
    if (res.status == 200) {
      setPassword("")
      setMessage("")
    }
    toast({
      title: data.title,
      description: data.description,
      status: data.status,
      duration: 9000,
      isClosable: true,
    })
  }

  return (
    <Layout>
        <Head>
          <title>Admin | Menu Sender</title>
          <meta name="description" content="Generated by create next app" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Container centerContent maxW='container.l' p={0}>
          <Text 
            bgGradient='linear(to-l, orange.400, orange.500)'
            bgClip='text'
            fontSize='6xl'
            fontWeight='extrabold'
          >Send It</Text>
          <Box my={6} w={"sm"} maxW={"100%"} borderRadius={12} borderWidth='1px' p={6} >
            <form onSubmit={(e) => submitForm(e)}>
              <Input value={password} type={"password"} placeholder="Super secret password" required onChange={(e : React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}/>
              <Textarea id='message' mt={2} placeholder='Custom Message' value={message} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setMessage(e.target.value)}/>
              <Button mt={2} type="submit">Send Menu Sender</Button>
            </form>
          </Box>
        </Container>
    </Layout>
  )
}

export default Admin
