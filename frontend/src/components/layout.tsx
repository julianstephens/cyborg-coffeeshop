import { currentUserAtom } from "@/atoms";
import { Avatar } from "@/components/ui/avatar";
import type { ChildrenProps } from "@/types";
import { Box, Container, Flex, Text } from "@chakra-ui/react";
import { useAtomValue } from "jotai";
import { useLocation, useNavigate } from "react-router";

const colorPalette = ["red", "blue", "green", "yellow", "purple", "orange"];

const Header = () => {
  const pickPalette = (name: string) => {
    const index = name.charCodeAt(0) % colorPalette.length;
    return colorPalette[index];
  };

  const { data: user } = useAtomValue(currentUserAtom);

  const goto = useNavigate();

  return (
    <Flex pb="4" width="full" justifyContent="space-between">
      <Text fontSize={"xl"} fontWeight={"bold"}>
        Cyborg Coffeeshop
      </Text>
      <Box>
        {user && user.full_name ? (
          <Avatar
            name={user.full_name}
            colorPalette={pickPalette(user.full_name)}
          />
        ) : (
          <Avatar
            cursor={"pointer"}
            transitionDuration={"slow"}
            _hover={{ shadow: "lg" }}
            onClick={() => {
              goto("/login");
            }}
          />
        )}
      </Box>
    </Flex>
  );
};

export const Layout = ({ children }: ChildrenProps) => {
  const { pathname } = useLocation();

  return (
    <Container
      id="layoutContainer"
      fluid={true}
      maxWidth={"full"}
      h="100%"
      padding={"8"}
    >
      {pathname != "/login" && <Header />}
      {children}
    </Container>
  );
};
