import type { NextPage } from 'next'
import Head from 'next/head'
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
  useToast
} from '@chakra-ui/react'
import { Formik, Form, Field } from 'formik'
import Layout from '../components/layout'
import { CheckRes } from '../lib/dateFormat'

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
                let res = await fetch(process.env.NEXT_PUBLIC_API_LEAD + "/recipient/unsubscribe", {
                    method: "POST",
                    body: JSON.stringify({
                      email : values.email
                    }),
                });
                let data : CheckRes = await res.json();
                toast({
                  title: data.title,
                  description: data.description,
                  status: data.status,
                  duration: 9000,
                  isClosable: true,
                })
                actions.setSubmitting(false)
                actions.resetForm({
                  values: {
                    email: ''
                  },
                });
              }}
            >
              {(props) => (
                <Form>
                  <Field name='email' validate={validateEmail}>
                    {({ field, form } : { field: any, form: any}) => (
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
