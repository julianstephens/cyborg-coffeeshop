import { accessTokenAtom, currentUserAtom } from "@/atoms";
import { Avatar } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  MenuContent,
  MenuItem,
  MenuRoot,
  MenuSeparator,
  MenuTrigger,
} from "@/components/ui/menu";
import type { ChildrenProps } from "@/types";
import { Box, Container, Flex, Text } from "@chakra-ui/react";
import { useAtom, useSetAtom } from "jotai";
import { RESET } from "jotai/utils";
import { useLocation, useNavigate } from "react-router";

const colorPalette = ["red", "blue", "green", "yellow", "purple", "orange"];

const Header = () => {
  const pickPalette = (name: string) => {
    const index = name.charCodeAt(0) % colorPalette.length;
    return colorPalette[index];
  };

  const [{ data: user, refetch }] = useAtom(currentUserAtom);
  const goto = useNavigate();
  const setAccessToken = useSetAtom(accessTokenAtom);

  const logout = () => {
    setAccessToken(RESET);
    refetch();
  };

  return (
    <>
      <Flex pb="4" width="full" justifyContent="space-between">
        <Text fontSize={"xl"} fontWeight={"bold"}>
          Cyborg Coffeeshop
        </Text>
        <Box>
          {user && user.full_name ? (
            <MenuRoot positioning={{ placement: "bottom-start" }}>
              <MenuTrigger asChild>
                <Button variant="plain" w="fit" _focus={{ outline: "none" }}>
                  <Avatar
                    name={user.full_name}
                    colorPalette={pickPalette(user.full_name)}
                    _hover={{
                      shadow: "lg",
                      shadowColor: pickPalette(user.full_name),
                    }}
                  />
                </Button>
              </MenuTrigger>
              <MenuContent>
                <MenuItem value="settings">Settings</MenuItem>
                <MenuSeparator />
                <MenuItem
                  value="logout"
                  fontWeight="bold"
                  onClick={(e) => {
                    e.preventDefault();
                    logout();
                  }}
                >
                  Logout
                </MenuItem>
              </MenuContent>
            </MenuRoot>
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
    </>
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
