import { Product } from "@/types";
import { Card } from "@chakra-ui/react";

export const ProductCard = ({ prod }: { prod: Product }) => (
  <Card.Root>
    <Card.Header>{prod.name}</Card.Header>
    <Card.Body>{prod.description ?? ""}</Card.Body>
    <Card.Footer>
      ${prod.price} {prod.currency}
    </Card.Footer>
  </Card.Root>
);
