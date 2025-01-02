import { productsAtom } from "@/atoms";
import { ProductCard } from "@/components/product";
import { For, Group, Text } from "@chakra-ui/react";
import { useAtom } from "jotai";

const StoreFront = () => {
  const [{ data, error, isLoading }] = useAtom(productsAtom);

  return (
    <>
      <Text fontSize={"xl"} py="8">
        Shop Now!
      </Text>
      <Group>
        {!isLoading && !error && data ? (
          <For each={data.data}>
            {(item, index) => <ProductCard key={index} prod={item} />}
          </For>
        ) : (
          "Failover"
        )}
      </Group>
    </>
  );
};

export default StoreFront;
