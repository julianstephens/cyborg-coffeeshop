import { productsAtom } from "@/atoms";
import { Loader } from "@/components/loader";
import { ProductCard } from "@/components/product";
import { Flex, For, SimpleGrid, Text } from "@chakra-ui/react";
import { useAtom } from "jotai";

const StoreFront = () => {
  const [{ data, error, isLoading }] = useAtom(productsAtom);

  return (
    <>
      <Text fontSize={"xl"} py="8">
        Shop Now!
      </Text>
      <SimpleGrid
        minChildWidth="xs"
        columnGap="10px"
        rowGap="40px"
        id="productGrid"
      >
        {!isLoading && !error && data ? (
          <For each={data.data}>
            {(item, index) => <ProductCard key={index} prod={item} />}
          </For>
        ) : (
          <Flex h="full" w="full" justifyContent="center" alignItems="center">
            <Loader />
          </Flex>
        )}
      </SimpleGrid>
    </>
  );
};

export default StoreFront;
