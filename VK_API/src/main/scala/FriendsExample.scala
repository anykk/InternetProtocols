import scala.util.{Success, Failure}

object FriendsExample extends ApiWrapper {
  private val onlineMap = Map(0 -> "yes", 1 -> "no")

  def getInfo(id: String): Seq[String] = {
    val resp = mkQuery("friends.get", "5.74",
      Seq(s"user_id=$id", "fields=online", "order=name"))
    resp match {
      case Success(responseElem) => (responseElem \\ "user").map { user =>
        s"""First name: ${user \\ "first_name" text}
           |Last name: ${user \\ "last_name" text}
           |Online: ${onlineMap((user \\ "online" text).toInt)}\n""".stripMargin
      }

      case Failure(exception) => Seq(s"Failed: ${exception.toString}")
    }
  }
}
