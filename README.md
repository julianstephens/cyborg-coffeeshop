# Cyborg Coffeeshop

## URLs

The production or staging URLs would use these same paths, but with your own domain.
Development URLs

### Development URLs, for local development.

| Resource                                | URL                                                        |
| --------------------------------------- | ---------------------------------------------------------- |
| Frontend                                | [http://localhost:5173](http://localhost:5173)             |
| Backend                                 | [http://localhost:8000](http://localhost:8000)             |
| Automatic Interactive Docs (Swagger UI) | [http://localhost:8000/docs](http://localhost:8000/docs)   |
| Automatic Alternative Docs (ReDoc)      | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| Adminer                                 | [http://localhost:8080](http://localhost:8080)             |
| Traefik UI                              | [http://localhost:8090](http://localhost:8090)             |
| MailCatcher                             | [http://localhost:1080](http://localhost:1080)             |

## Order Workflow

1. User adds items to cart
2. User selects cart items to checkout with
3. User fills out stripe embedded form
4. Stripe authorizes payment
5. System creates order and updates stock
6. Payment captured
7. System redirects user to order confirmation
