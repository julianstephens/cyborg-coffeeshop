import { productsAtom } from "@/atoms";
import { ProductCard } from "@/components/product";
import { Flex, For } from "@chakra-ui/react";
import { useAtom } from "jotai";
import { useEffect } from "react";

const StoreFront = () => {
  const [{ data, error, isLoading }] = useAtom(productsAtom);

  useEffect(() => {
    if (!error && !isLoading && data) {
      console.log(data);
    }
  }, []);

  return (
    <Flex>
      {!isLoading && !error && data ? (
        <For each={data.data}>
          {(item, index) => <ProductCard key={index} prod={item} />}
        </For>
      ) : (
        "Failover"
      )}
    </Flex>
  );
};

export default StoreFront;
