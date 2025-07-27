# rimo-frontend

[オンボーディングドキュメント 開発メンバー向け確認ページ](./docs/onboarding/rimo_developer_onboarding.md)

## 開発方法

- [ドキュメント](docs/)

## 実行方法

```
pnpm install
pnpm dev または pnpm dev:https
```

## 新しいUIコンポーネントの実装方法

私たちはMUI（material-ui）の代わりに`shadcn/ui`と`tailwind`を使用することを決定しました。これからはそれらを使用することが求められます。基本的に、MUIで作成されたプルリクエストを承認することはできません。MUIを使用したい場合は、私たちに承認を求めてください。

## admin-appの実行方法

admin-appはクライアント/サーバー側のFirebase認証を使用しています。つまり、現在は独自に資格情報を設定する必要があります。
クライアント側にエクスポートする環境変数としてfirebase-admin資格情報ファイルを指定されたパスに置く必要があります。（サーバー側は設定不要です。）

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/objects/rimo-dev-0.json"
cat $GOOGLE_APPLICATION_CREDENTIALS
```

```bash
pnpm install
pnpm dev:admin
```

## FAQ

### ローカルで起動したrimo-backendと統合する

ローカルで起動した[rimo-backend](https://github.com/rimoapp/rimo-backend)に接続したい場合は、以下のコマンドを実行してください。

- <root>/.envフィールドの`NEXT_PUBLIC_RIMO_BACKEND_URL`を編集

```diff
- NEXT_PUBLIC_RIMO_BACKEND_URL=https://rimo-backend.rimo-stg.app
+ NEXT_PUBLIC_RIMO_BACKEND_URL=http://localhost:8080
```

### ブラウザが自動でhttpからhttpsにリダイレクトまたはその逆になる

おそらくHSTSが原因です。その場合は、`chrome://net-internals/#hsts`を訪れてキャッシュをクリアする必要があります。

[ドメインセキュリティポリシーの削除]のドメインフィールドに`localhost`を入力し、[削除]ボタンをクリックします。成功したかどうかは[HSTS/PKPドメインをクエリ]セクションで確認できます。

### 両方のアプリを起動する

次のコマンドで全てのサーバーを起動できます。

```
pnpm dev:all
```

### 特殊オプションのChromeを準備する

http://localhost:3000/servers/xxxを実行したい場合は、Google Chromeの`no-user-gesture-required`バージョンを使用する必要があります。
Macでこれを実行するには：

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --autoplay-policy=no-user-gesture-required
```

## Dockerで実行する方法

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

そしてhttp://localhost:4400を開きます。

## ダークモードについて
[dark-mode.md](docs/dark-mode.md)を参照してください。