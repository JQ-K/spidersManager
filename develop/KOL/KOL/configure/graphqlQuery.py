videoFeedsQuery = {
    "operationName": "videoFeedsQuery",
    "variables": {
        "count": 20,
        "pcursor": "0"
    },
    "query": "fragment VideoMainInfo on VideoFeed {\n  photoId\n  caption\n  thumbnailUrl\n  poster\n  viewCount\n  likeCount\n  commentCount\n  timestamp\n  workType\n  type\n  useVideoPlayer\n  imgUrls\n  imgSizes\n  magicFace\n  musicName\n  location\n  liked\n  onlyFollowerCanComment\n  width\n  height\n  expTag\n  __typename\n}\n\nquery videoFeedsQuery($pcursor: String, $count: Int) {\n  videoFeeds(pcursor: $pcursor, count: $count) {\n    list {\n      user {\n        id\n        eid\n        profile\n        name\n        __typename\n      }\n      ...VideoMainInfo\n      __typename\n    }\n    pcursor\n    __typename\n  }\n}\n"
}


publicFeedsQuery = {
    "operationName": "publicFeedsQuery",
    "variables": {
        "principalId": "3xy424mqbve5h82",
        "pcursor": "0",
        "count": 240
    },
    "query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        kwaiId\n        eid\n        profile\n        name\n        living\n        __typename\n      }\n      watchingCount\n      src\n      title\n      gameId\n      gameName\n      categoryId\n      liveStreamId\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      followed\n      type\n      living\n      redPack\n      liveGuess\n      anchorPointed\n      latestViewed\n      expTag\n      __typename\n    }\n    list {\n      photoId\n      caption\n      thumbnailUrl\n      poster\n      viewCount\n      likeCount\n      commentCount\n      timestamp\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      width\n      height\n      user {\n        id\n        eid\n        name\n        profile\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
}


commentListQuery = {
    "operationName": "commentListQuery",
    "variables": {
        "pcursor": "0",
        "photoId": "3xz7aiwh5tgc3x9",
        "page": 1,
        "count": 200
    },
    "query": "query commentListQuery($photoId: String, $page: Int, $pcursor: String, $count: Int) {\n  shortVideoCommentList(photoId: $photoId, page: $page, pcursor: $pcursor, count: $count) {\n    commentCount\n    realCommentCount\n    pcursor\n    commentList {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      authorEid\n      status\n      subCommentCount\n      subCommentsPcursor\n      likedCount\n      liked\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        authorEid\n        status\n        replyToUserName\n        replyTo\n        replyToEid\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}


userInfoQuery = {
    "operationName": "userInfoQuery",
    "variables": {
        "principalId": "3xyt9e29tmjjixu"
    },
    "query": "query userInfoQuery($principalId: String) {\n  userInfo(principalId: $principalId) {\n    id\n    principalId\n    kwaiId\n    eid\n    userId\n    profile\n    name\n    description\n    sex\n    constellation\n    cityName\n    living\n    watchingCount\n    isNew\n    privacy\n    feeds {\n      eid\n      photoId\n      thumbnailUrl\n      timestamp\n      __typename\n    }\n    verifiedStatus {\n      verified\n      description\n      type\n      new\n      __typename\n    }\n    countsInfo {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    bannedStatus {\n      banned\n      defriend\n      isolate\n      socialBanned\n      __typename\n    }\n    __typename\n  }\n}\n"
}