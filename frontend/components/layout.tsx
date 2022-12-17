import { Box, Container, Heading, Text, Link } from "@chakra-ui/react"
import { ExternalLinkIcon } from '@chakra-ui/icons'
import { ReactNode } from 'react';

export default function Layout({ children } : { children : ReactNode }) {
  return (
    <>
    <Box minHeight={'100vh'} display={"flex"} flexDir={'column'}>
        <Box p='6' borderBottom={'3px solid #E57B2C'}>
            <Heading
            bgGradient='linear(to-l, orange.400, orange.500)'
            bgClip='text'
            fontSize='4xl'
            fontWeight='extrabold'>Menu Sender</Heading>
            <Text color={"gray.500"}>Get the hall menu in your inbox</Text>
        </Box>
        <Container flexGrow={1} my={4} maxW='container.md'>
            {children}
        </Container>
        <Box bgGradient='linear(to-l, orange.400, orange.500)' p={2} color={"white"} >
            <Text mx={10}>If you have any problems, just email <Link href='mailto:menu@exeter.oxtickets.co.uk' isExternal textDecor={"underline"}>
            menu@exeter.oxtickets.co.uk<ExternalLinkIcon mx='2px' />
            </Link>
            </Text>
        </Box>
    </Box>
    </>
  )
}