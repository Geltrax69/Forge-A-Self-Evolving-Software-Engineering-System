url: https://18.react.dev/
----

# React

The library for web and native user interfaces

[Learn React](/learn)[API Reference](/reference/react)

## Create user interfaces from components

React lets you build user interfaces out of individual pieces called components. Create your own React components like `Thumbnail`, `LikeButton`, and `Video`. Then combine them into entire screens, pages, and apps.

### Video.js

```
function Video({ video }) {

  return (

    <div>

      <Thumbnail video={video} />

      <a href={video.url}>

        <h3>{video.title}</h3>

        <p>{video.description}</p>

      </a>

      <LikeButton video={video} />

    </div>

  );

}
```

```
function VideoList({ videos, emptyHeading }) {

  const count = videos.length;

  let heading = emptyHeading;

  if (count > 0) {

    const noun = count > 1 ? 'Videos' : 'Video';

    heading = count + ' ' + noun;

  }

  return (

    <section>

      <h2>{heading}</h2>

      {videos.map(video =>

        <Video key={video.id} video={video} />

      )}

    </section>

  );

}
```

```
import { useState } from 'react';



function SearchableVideoList({ videos }) {

  const [searchText, setSearchText] = useState('');

  const foundVideos = filterVideos(videos, searchText);

  return (

    <>

      <SearchInput

        value={searchText}

        onChange={newText => setSearchText(newText)} />

      <VideoList

        videos={foundVideos}

        emptyHeading={`No matches for “${searchText}”`} />

    </>

  );

}
```

----------------

React is a library. It lets you put components together, but it doesn’t prescribe how to do routing and data fetching. To build an entire app with React, we recommend a full-stack React framework like [Next.js](https://nextjs.org) or [Remix](https://remix.run).

### confs/\[slug].js

```
import { db } from './database.js';

import { Suspense } from 'react';



async function ConferencePage({ slug }) {

  const conf = await db.Confs.find({ slug });

  return (

    <ConferenceLayout conf={conf}>

      <Suspense fallback={<TalksLoading />}>

        <Talks confId={conf.id} />

      </Suspense>

    </ConferenceLayout>

  );

}



async function Talks({ confId }) {

  const talks = await db.Talks.findAll({ confId });

  const videos = talks.map(talk => talk.video);

  return <SearchableVideoList videos={videos} />;

}
```

[Get started with a framework](/learn/start-a-new-react-project)

## Use the best from every platform

People love web and native apps for different reasons. React lets you build both web apps and native apps using the same skills. It leans upon each platform’s unique strengths to let your interfaces feel just right on every platform.

example.com

#### Stay true to the web

People expect web app pages to load fast. On the server, React lets you start streaming HTML while you’re still fetching data, progressively filling in the remaining content before any JavaScript code loads. On the client, React can use standard web APIs to keep your UI responsive even in the middle of rendering.

5:15 PM

## [React Compiler Beta Release and Roadmap](/blog/2024/10/21/react-compiler-beta-release)

[October 21, 2024](/blog/2024/10/21/react-compiler-beta-release)

## [React Conf 2024 Recap](/blog/2024/05/22/react-conf-2024-recap)

[May 22, 2024](/blog/2024/05/22/react-conf-2024-recap)

## [React 19 RC](/blog/2024/04/25/react-19)

[April 25, 2024](/blog/2024/04/25/react-19)

## [React 19 RC Upgrade Guide](/blog/2024/04/25/react-19-upgrade-guide)

[April 25, 2024](/blog/2024/04/25/react-19-upgrade-guide)

[Read more React news](/blog)

Join a community\
of millions
-----------

You’re not alone. Two million developers from all over the world visit the React docs every month. React is something that people and teams can agree on.

This is why React is more than a library, an architecture, or even an ecosystem. React is a community. It’s a place where you can ask for help, find opportunities, and meet new friends. You will meet both developers and designers, beginners and experts, researchers and artists, teachers and students. Our backgrounds may be very different, but React lets us all create user interfaces together.

Welcome to the\
React community
---------------

[Get Started](/learn)

----
