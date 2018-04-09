import scala.io.StdIn
import scala.xml._

//116951205

object Main extends App {
  def onlineMap = Map("0" -> "yes", "1" -> "no")

  def friends = (id: String) => Wrapper.mkQuery("friends.get", "5.74",
    Seq(s"user_id=$id", "fields=online", "order=name")).getOrElse(
    <response></response>.mkString)

  override def main(args: Array[String]): Unit = {
    val id = StdIn.readLine("Enter user's id: ")
    val responseElem = XML.loadString(friends(id))
    (responseElem \\ "user").foreach {user =>
      println(
        s"""First name: ${user \\ "first_name" text}
           |Last name: ${user \\ "last_name" text}
           |Online: ${onlineMap(user \\ "online" text)}\n""".stripMargin)
    }
  }
}