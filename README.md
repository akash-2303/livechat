
# YouTube Debate Comments Dataset JSON Schema

This README describes the structure of a JSON dataset comprising YouTube comments collected from presidential and vice-presidential debate videos.

## File Structure

Each JSON object represents an individual comment, providing metadata such as author details, engagement metrics, and contextual identifiers for debate type and collection details.

## JSON Schema

### Sample JSON Object

```json
{
    "author": "@BabyLolaRazz",
    "authorProfileImageUrl": null,
    "authorChannelUrl": null,
    "text": "Topic: coronavirus pandemic- hey hi 👋, USA didn’t have a break out of the H1N1 because of me/Desi. 😅 the ungratefulness in this country.",
    "likeCount": 0,
    "published_at": "2024-08-27T14:14:40Z",
    "updatedAt": null,
    "canRate": null,
    "viewerRating": null,
    "isPublic": true,
    "Source": "Sky",
    "collector": "Akash, Deeptika & Priyanshu",
    "debate_type": "P",
    "type": "comment"
}
```

### Field Descriptions

| Field                  | Type       | Description                                                                                       |
|------------------------|------------|---------------------------------------------------------------------------------------------------|
| `author`               | `String`   | The username of the comment author.                                                               |
| `authorProfileImageUrl`| `String`   | URL to the author’s profile image, `null` if unavailable.                                         |
| `authorChannelUrl`     | `String`   | URL to the author’s profile/channel, `null` if unavailable.                                       |
| `text`                 | `String`   | The content of the comment, which may include emojis and special characters.                      |
| `likeCount`            | `Integer`  | The number of likes the comment has received.                                                     |
| `publishedAt`         | `DateTime` | Timestamp in ISO 8601 format (e.g., `2024-08-27T14:14:40Z`) indicating when the comment was posted. |
| `updatedAt`            | `DateTime` | Timestamp of the last update; `null` if not updated.                                              |
| `canRate`              | `Boolean`  | Specifies if viewers can rate (e.g., like/dislike) the comment.                                   |
| `viewerRating`         | `String`   | Viewer’s rating on the comment, such as "like" or "dislike"; `null` if unavailable.               |
| `isPublic`             | `Boolean`  | Indicates if the comment is public (`true`) or private (`false`).                                 |
| `Source`               | `String`   | Platform or channel from which the comment originated (e.g., "Sky").                              |
| `collector`            | `String`   | Custom field indicating the data collection team: 'Akash & Deeptika' 'Priyanshu' 'Deeptika & Priyanshu' 'Deeptika', etc.                  |
| `debate_type`          | `String`   | Specifies the debate type, with "P" for presidential debates and "VP" for vice-presidential debates. |
| `type`                 | `String`   | Type of content, which can be `comment` or `livechat`.                                            |

### Field Notes

- **Null Fields**: Fields like `authorProfileImageUrl`, `authorChannelUrl`, `updatedAt`, `canRate`, and `viewerRating` may be `null` if data is unavailable.
- **DateTime Fields**: `published_at` and `updatedAt` are in ISO 8601 format. `updatedAt` remains `null` if the comment has not been edited post-publication.
- **Custom Fields**:
  - `debate_type`: Specifies the debate type—"P" for presidential debates and "VP" for vice-presidential debates.
  - `type`: Indicates the nature of the interaction, either `comment` or `livechat`.
  - `collector`: Identifies the collection team members (Akash, Deeptika & Priyanshu).
  - `Source`: Identifies the youtube channel(news network) name of the comment.

Here’s the enhanced section for the README file explaining the conversion process to the merged JSON schema:

---

## Conversion to Merged JSON Schema

### 1. Livechat Conversion
- **Collection Method**: Live chat data was collected using the pytchat library, which allows real-time scraping of YouTube live chat messages.

- **Original Attributes**: `author`, `timestamp`, and `message`
- **Converted Attributes**:
  - `timestamp` ➔ `publishedAt`
  - `message` ➔ `text`

This conversion standardizes live chat messages with other comment data, aligning timestamps and text content fields with a consistent naming convention.

### 2. Historic Data Conversion
- **Collection Method**: Comments from the 2020 and 2024 presidential debates (featuring Biden and Trump) were collected and stored initially in CSV format.

- **Original Attributes**: `author`, `published_at`, `like_count`, `text`, and `public`

- **Converted Attributes**:
  - `published_at` ➔ `publishedAt`
  - `like_count` ➔ `likeCount`
  - `public` ➔ `isPublic`

This standardized naming allows seamless integration with live chat and other comment data types, supporting analysis across debates and data formats.

### 3. Comments Conversion

- **Collection Method**: Comments were collected directly using the YouTube Data API.

- **Attributes**:
  - `author`
  - `authorChannelUrl`
  - `text`
  - `likeCount`
  - `publishedAt`
  - `updatedAt`
  - `canRate`
  - `viewerRating`
  - `isPublic`
  - `authorProfileImageUrl`

## Data Collection

Data was collected by **Akash, Deeptika & Priyanshu** using public YouTube comments and live chats from debate videos. The `collector` field records the data collection team for transparency.

## Licensing

This dataset is intended solely for research and analytical purposes. Users should adhere to all applicable data privacy laws and YouTube’s terms of service when using this dataset.


 

