import type { NextPage } from 'next'
import Head from 'next/head'
import styles from '../styles/Home.module.css'
import {
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
  Input,
  Button,
  Box,
  Container,
  Text,
  Checkbox,
  useToast
} from '@chakra-ui/react'
import { Formik, Form, Field } from 'formik'
import type { ReactElement } from 'react'
import Layout from '../components/layout'
import { EmailIcon } from '@chakra-ui/icons'

const Unsub: NextPage = () => {

  function validateEmail(value : string) {
    let error
    if (!value) {
      error = 'Required';
    } else if (!/^[A-Z0-9._%+-]+@exeter.ox.ac.uk$/i.test(value)) {
      error = 'Invalid email address';
    }
    return error
  }
  function validateCheck(value : string) {
    let error
    if (!value) {
      error = 'Required';
    }
    return error
  }


  const toast = useToast()
  
  return (
    <Layout>
        <Head>
          <title>Unsubscribe from Menu Sender</title>
          <meta name="description" content="Unsubscribe from the Exeter College Oxford Dinner Menu" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Container centerContent maxW='container.l' p={0}>
          <Text 
            bgGradient='linear(to-l, orange.400, orange.500)'
            bgClip='text'
            fontSize='4xl'
            fontWeight='extrabold'
          >Unsubscribe</Text>
          <Text>Please do not go. I&apos;ll be better.</Text>
          <Box my={6} w={"sm"} maxW={"100%"} borderRadius={12} borderWidth='1px' p={6} >
            <Formik
              initialValues={{ email : ""}}
              onSubmit = { async (values : { email: string }, actions) => {
                let route = [process.env.API_LEAD, "/api/unsubscribe"].join('')
                let res = await fetch(route, {
                    method: "POST",
                    body: JSON.stringify({
                      email : values.email
                    }),
                });
                res = await res.json();
                console.log(res)
                if (res.deletedCount === 0) {
                  let name = values.email.split(".")[0];
                  name = name.charAt(0).toUpperCase() + name.slice(1);
                  toast({
                    title: 'Oops ' + name,
                    description: "Looks like you were never on the list.",
                    status: 'warning',
                    duration: 9000,
                    isClosable: true,
                  })
                } else {
                  let name = values.email.split(".")[0];
                  name = name.charAt(0).toUpperCase() + name.slice(1);
                  toast({
                    title: 'I am sad to see you go ' + name,
                    description: "There won't be any more emails from now on.",
                    status: 'success',
                    duration: 9000,
                    isClosable: true,
                  })
                }
                setTimeout(() => {
                  actions.setSubmitting(false)
                  actions.resetForm({
                    values: {
                      email: ''
                    },
                  });
                }, 1000)
              }}
            >
              {(props) => (
                <Form>
                  <Field name='email' validate={validateEmail}>
                    {({ field, form }) => (
                      <>
                      <FormControl isInvalid={form.errors.email && form.touched.email}>
                        <FormLabel htmlFor='email'>College Email Address</FormLabel>
                        <Input {...field} type="email" id='email' placeholder='College Email' />
                        <FormHelperText>the one ending in @exeter.ox.ac.uk</FormHelperText>
                        <FormErrorMessage>{form.errors.email}</FormErrorMessage>
                      </FormControl>
                      </>
                    )}
                  </Field>  
                  <Button
                    mt={4}
                    colorScheme='orange'
                    isLoading={props.isSubmitting}
                    type='submit'
                    loadingText='Submitting'
                  >
                    Unsubscribe
                  </Button>
                </Form>
              )}
            </Formik>
          </Box>
        </Container>
    </Layout>
  )
}

export default Unsub
