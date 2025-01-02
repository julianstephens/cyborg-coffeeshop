import productPlaceholder from "@/assets/product-placeholder.png";
import { $api } from "@/client";
import type { Product, ProductReviews, Review } from "@/types";
import {
  Badge,
  Box,
  Flex,
  For,
  HStack,
  Icon,
  Image,
  Text,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { HiStar } from "react-icons/hi";

const Ratings = ({ reviews }: { reviews?: Review[] }) => {
  return (
    <>
      {reviews && reviews?.length > 0 && (
        <HStack gap="1" fontWeight="medium">
          <Icon color="orange.400">
            <HiStar />
          </Icon>
          <Text>
            {reviews.map((r) => r.rating).reduce((a, b) => a + b, 0) /
              reviews.length}{" "}
            ({reviews.length})
          </Text>
        </HStack>
      )}
    </>
  );
};

export const ProductCard = ({ prod }: { prod: Product }) => {
  const [productReviews, setReviews] = useState<ProductReviews>({});
  const { data, error, isLoading } = $api.useQuery("get", "/api/v1/reviews/", {
    params: { query: { product: prod.id } },
  });

  useEffect(() => {
    const pid = prod.id;
    if (!pid) return;

    if (!isLoading && !error && data) {
      setReviews((prev) => {
        if (prev[pid]) {
          return {
            ...prev,
            [pid]: [...prev[pid], ...data.data],
          };
        }
        return { ...prev, [pid]: data.data };
      });
    }
  }, [data]);

  return (
    <Box maxW={"xs"} borderWidth={"1px"}>
      <Image src={productPlaceholder} alt={prod.name} />
      <Box p={"2"} spaceY="2">
        <Flex justifyContent={"space-between"}>
          <Text fontWeight={"medium"}>{prod.name}</Text>
          <Text color="fg.muted">
            ${prod.price} {prod.currency}
          </Text>
        </Flex>
        <HStack p="0">
          {prod.categories.length > 0 && (
            <For each={prod.categories}>
              {(item) => <Badge bg={`${item.color}.500`}>{item.name}</Badge>}
            </For>
          )}
          <Ratings reviews={productReviews[prod.id!]} />
        </HStack>
      </Box>
    </Box>
  );
};
