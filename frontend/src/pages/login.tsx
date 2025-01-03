import { accessTokenAtom, currentUserAtom } from "@/atoms";
import { $api } from "@/client";
import { Button } from "@/components/ui/button";
import { PasswordInput } from "@/components/ui/password-input";
import { toaster } from "@/components/ui/toaster";
import type { LoginRequest } from "@/types";
import { isAPIError } from "@/utils";
import { Flex, Input, Text } from "@chakra-ui/react";
import { useForm } from "@tanstack/react-form";
import { useAtom, useSetAtom } from "jotai";
import { useEffect } from "react";
import { useNavigate } from "react-router";

const Login = () => {
  const [{ data: currentUser, isLoading, error }, setCurrentUser] =
    useAtom(currentUserAtom);
  const setAccessToken = useSetAtom(accessTokenAtom);
  const goto = useNavigate();
  const { mutateAsync } = $api.useMutation(
    "post",
    "/api/v1/login/access-token"
  );

  useEffect(() => {
    if (!isLoading && !error && currentUser) {
      goto("/");
    }
  }, [isLoading]);

  const { Field, handleSubmit } = useForm<LoginRequest>({
    defaultValues: {
      username: "",
      password: "",
      scope: "",
    },
    onSubmit: async ({ value }) => {
      try {
        const res = await mutateAsync({
          body: value,
          bodySerializer: (body) => {
            const jsonBody = JSON.parse(JSON.stringify(body));
            const fd = new FormData();
            for (const name in jsonBody) {
              fd.append(name, jsonBody[name]);
            }
            return fd;
          },
        });
        setAccessToken(res.access_token);
        if (currentUser) setCurrentUser();
        goto("/");
      } catch (err: unknown) {
        if (isAPIError(err)) {
          if (err.detail && Array.isArray(err.detail)) {
            err.detail.forEach((e) => {
              toaster.create({
                title: e.msg,
                type: "error",
              });
            });
            return;
          }

          if (err.detail && typeof err.detail == "string") {
            toaster.create({
              title: err.detail,
              type: "error",
            });
          }
        }
      }
    },
  });
  return (
    <Flex
      id="loginFormBox"
      h="full"
      w="full"
      align="center"
      direction="column"
      justify="center"
    >
      <Text fontSize="2xl" fontWeight="bold" w="fit" mx="auto" mb="8">
        Cyborg Coffeeshop
      </Text>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        <Flex direction="column" gap="4" id="loginFormFieldsBox" mb="8">
          <Field
            name="username"
            children={(field) => (
              <>
                <Input
                  placeholder="Email"
                  w="80"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  required
                />
              </>
            )}
          />
          <Field
            name="password"
            children={(field) => (
              <>
                <PasswordInput
                  placeholder="Password"
                  w="80"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  required
                />
              </>
            )}
          />
        </Flex>
        <Button
          type="submit"
          w="80"
          color="white"
          fontWeight="bold"
          bg="green.600"
          _hover={{ shadow: "lg", shadowColor: "green.500", bg: "green.500" }}
        >
          Log In
        </Button>
      </form>
    </Flex>
  );
};

export default Login;
