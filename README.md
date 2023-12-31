# RPG Notes

Try keeping notes in markdown so we can build them into a website.

The notes are found in the `docs/` folder, and are all markdown files. They can
be edited in the browser or locally.

## How to edit

All of the notes rendered on the website live in the `docs/` folder. These are
all written in markdown, which is a light markup language. See
[here](https://www.markdownguide.org/cheat-sheet) for an overview of the syntax.
You can edit the files directly in your browser, which is probably the most
straightforward, or locally, in which case you'll have to set up git.

For any file, a little "edit this page" button will appear next to the title.
Click on it to start editing it on github!

Once you edit any file, you'll have to commit it (for a little bit more about
git and what the terminology means, see
[here](https://neuroplausible.com/github)). Doing so will trigger the website to
rebuild, the progress of which can be seen on the [actions
tab](https://github.com/billbrod/rpg_notes/actions). After about 2 minutes, the
website will be finished any changes should be live.

To add inline images, upload them to the `docs/images/` folder and then include
a link like so: `![Alternative text](./images/my_awesome_image.png "Text that
appears when hovering")`.

The website is built using [mkdocs](https://www.mkdocs.org/). If you add a new
page, you'll need to add it to the `nav:` section of the `mkdocs.yml` file.

We use the [mkdocs
material](https://squidfunk.github.io/mkdocs-material/reference/) theme, which
gives all sorts of extra features like better tables and admonitions. Check out
that link for more details!

## Development

(These are my notes as to how I got this set up, not necessary for anyone else)

### DM Notes

The DM notes live in a separate, private repo, connected as a submodule.
Following the instructions
[here](https://ehlers.berlin/blog/private-submodules-in-github-ci/):
- The idea is to create a new pair of keys: `ssh-keygen -t rsa -f key`
- Make the public key the deploy key for the private repo: in the private repo,
  go to `Settings > Deploy keys`, and copy the public key there.
- Add the private key as a secret key on the public repo: in the public repo, go
  to `Settings > Secrets > Actions` and add the private key.
- Then the following step should allow the deploy job in the public repo to pull
  in the private one:

  ```yml
  - name: Trigger release build
    env:
      SSH_KEY_FOR_SUBMODULE: ${{secrets.SSH_KEY_FOR_SUBMODULE}}
    run: |
      mkdir $HOME/.ssh && echo "$SSH_KEY_FOR_SUBMODULE" > $HOME/.ssh/id_rsa && chmod 600 $HOME/.ssh/id_rsa && git submodule update --init --recursive
 ```

### DM note filtering

The python script `filter_dm.py` will filter out any sections with the tag
`:dm:` in the header and is used before the build action. It operates on
stdin/stdout, so should be used like so:

``` sh
pandoc file.md -t json | python filter_dm.py | pandoc -f json -t gfm -o filtered.md
```

If a file exists with the same name in the public `docs/` directory, combine
them gracefully, so they're merged rather than one overwriting the other.

### Netlify

We deploy to netlify so that we can hide the DM-only notes behind a login. The
website is deployed to Netlify using the action `.github/workflows/deploy.yml`.
We use the Netlify Identity widget to handle logins, which required the
following steps:
- [enable identity](https://docs.netlify.com/visitor-access/identity/) via the
  integrations tab
- Creating the actual login button is done as discussed
  [here](https://www.netlify.com/blog/2018/01/23/getting-started-with-jwt-and-identity/),
  adding extra javascript and overriding the announce block to add the actual
  login button itself.
- set registration to invite-only under `Site configuration > Identity >
  Registration`.
  
Then, to add users:
- Go to `Integrations > Identity`, to invite users and set their role
- They'll get an email, which they should follow and will prompt them to create
  a password
  - I also configured this to accept Github authentication.
  
The actual hiding of information is done via [role-based
redirects](https://docs.netlify.com/visitor-access/role-based-access-control/),
as defined in the `netlify.toml` file in this repo. Anyone who doesn't have the
role `dm` will only see a "404" page when they go to `/dm` on the website.
