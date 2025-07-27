# rimo-frontend

[onboarding_doc 開発メンバー向け確認ページ](./docs/onboarding/rimo_developer_onboarding.md)

## How to develop

- [docs](docs/)

## How to run

```
pnpm install
pnpm dev or pnpm dev:https
```

## How to implement new UI components

we make a decision to use `shadcn/ui` and `tailwind` instead of MUI(material-ui). it forces you to use them from now on. we basically can't approve your pull-requests made by MUI. Please ask us for approval if you want to use MUI.

## How to run admin-app

admin-app uses client/server side Firebase Authentication. that means we have to set up credentials by own currently.
it requires to put firebase-admin credential file object specified path with exporting env for client side. (no needed to set up for server side.)

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/objects/rimo-dev-0.json"
cat $GOOGLE_APPLICATION_CREDENTIALS
```

```bash
pnpm install
pnpm dev:admin
```

## FAQ

### Integrate rimo-backend locally launched

If you want to connect to a locally launched [rimo-backend](https://github.com/rimoapp/rimo-backend), run the following command

- edit <root>/.env `NEXT_PUBLIC_RIMO_BACKEND_URL` field

```diff
- NEXT_PUBLIC_RIMO_BACKEND_URL=https://rimo-backend.rimo-stg.app
+ NEXT_PUBLIC_RIMO_BACKEND_URL=http://localhost:8080
```

### Browser automatically redirect http to https or vice versa

it probably causes of HSTS. Then you should visit `chrome://net-internals/#hsts` to clear cache.

Input `localhost` into [Delete domain security policies]'s domain field and click [Delete] button. you can check if it succeeded with [Query HSTS/PKP domain] section.

### Launch both apps

you can start all servers by the following command.

```
pnpm dev:all
```

### Prepare special option Chrome

if you want to run http://localhost:3000/servers/xxx, you must use `no-user-gesture-required` version of Google Chrome.
To run this on Mac:

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --autoplay-policy=no-user-gesture-required
```

## How to run by docker

```
docker build . -t rimo-frontend
docker run --rm -p 3000:8080 rimo-frontend
open http://localhost:3000
```

## Storybook
```
pnpm storybook:ui
```
http://localhost:4402/


```
pnpm storybook
```

And open http://localhost:4400

## About DarkMode
See [dark-mode.md](docs/dark-mode.md)
